import json
from moxn.telemetry.client import TelemetryClient
import logging
from functools import lru_cache
from pathlib import Path
import httpx

from moxn.exceptions import MoxnSchemaValidationError
from moxn.models.prompt import Prompt, PromptInstance, RenderableModel
from moxn.models.schema import PromptSchemas, SchemaPromptType, CodegenResponse
from moxn.models.task import Task
from moxn.polling import PollingConfig, PollingManager
from moxn.storage.storage import InMemoryStorage
from moxn.base_models.telemetry import (
    SpanEventLogRequest,
    SpanLogRequest,
    TelemetryLogResponse,
    LLMEvent,
    SignedUrlRequest,
    SignedUrlResponse,
)
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Literal
from uuid import UUID

from moxn.telemetry.backend import HttpTelemetryBackend
from moxn.telemetry.context import SpanContext
from moxn.settings import MoxnSettings

logger = logging.getLogger(__name__)


class MoxnClient:
    """
    Moxn API client for interacting with the Moxn platform.

    Example:
        ```python
        client = MoxnClient(
            user_id="user123",
            org_id="org456",  # Optional
            api_key="sk-...",
            base_api_route="https://api.moxn.com/v1"
        )
        ```
    Example:
        ```python
        config = PollingConfig(
            interval=3600.0,  # Poll every hour
            versions_to_track={
                "task_123": ["v1", "v2"],
                "task_456": ["v1"],
            }
        )

        async with MoxnClient() as client:
            await client.start_polling(config)
        ```
    """

    def __init__(self) -> None:
        self.settings = MoxnSettings()  # type: ignore
        self._client: httpx.AsyncClient | None = None
        self.storage = InMemoryStorage()
        self._polling_manager: PollingManager | None = None
        self._context_depth = 0  # Track nested context usage

        backend = HttpTelemetryBackend.from_settings(self.settings)
        self.telemetry_client = TelemetryClient(backend=backend)

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client, creating it if necessary."""
        if self._client is None:
            self._client = self._create_client()
        return self._client

    def _create_client(self) -> httpx.AsyncClient:
        """Creates an authenticated httpx client."""
        return httpx.AsyncClient(
            base_url=str(self.settings.base_api_route),
            timeout=self.settings.timeout,
            headers=self.get_headers(),
        )

    @lru_cache(maxsize=1)
    def get_headers(self, _: bool = True) -> dict:
        """Returns the default headers for API prompts."""
        headers = {
            "x-api-key": self.settings.api_key.get_secret_value(),
            "x-requested-user-id": self.settings.user_id,
        }
        if self.settings.org_id:
            headers["x-requested-org-id"] = self.settings.org_id
        return headers

    async def __aenter__(self) -> "MoxnClient":
        self._context_depth += 1
        if self._client is None:
            self._client = self._create_client()
        await self.telemetry_client.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        self._context_depth -= 1
        if self._context_depth == 0:
            await self.telemetry_client.stop()
            await self.stop_polling()
            await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    async def get(self, path: str, **kwargs) -> httpx.Response:
        """Perform a GET prompt."""
        return await self.client.get(path, **kwargs)

    async def post(self, path: str, **kwargs) -> httpx.Response:
        """Perform a POST prompt."""
        return await self.client.post(path, **kwargs)

    async def put(self, path: str, **kwargs) -> httpx.Response:
        """Perform a PUT prompt."""
        return await self.client.put(path, **kwargs)

    async def delete(self, path: str, **kwargs) -> httpx.Response:
        """Perform a DELETE prompt."""
        return await self.client.delete(path, **kwargs)

    async def start_polling(self, config: PollingConfig) -> None:
        """Start polling for new versions of tasks and prompts."""
        if self._polling_manager is not None:
            await self._polling_manager.stop()

        self._polling_manager = PollingManager(
            config=config,
            fetch_task=self.fetch_task,
            fetch_prompt=self.fetch_prompt,
            store_task=self.storage.store_task,
            store_prompt=self.storage.store_prompt,
            get_last_polled=self.storage.get_last_polled,
            update_last_polled=self.storage.update_last_polled,
        )
        await self._polling_manager.start()

    async def stop_polling(self) -> None:
        """Stop polling for updates."""
        if self._polling_manager:
            await self._polling_manager.stop()
            self._polling_manager = None

    async def fetch_task(self, task_id: str, version_id: str | None = None) -> Task:
        """
        Fetch a task from the API.
        If version_id is None, fetches the latest version.
        """
        params = {}
        if version_id:
            params["version_id"] = version_id

        response = await self.get(f"/tasks/{task_id}", params=params)
        response.raise_for_status()

        return Task.model_validate(response.json())

    async def fetch_prompt(
        self, prompt_id: str, version_id: str | None = None
    ) -> Prompt:
        """
        Fetch a prompt from the API.
        If version_id is None, fetches the latest version.
        """
        params = {}
        if version_id:
            params["version_id"] = version_id

        response = await self.get(f"/prompts/{prompt_id}", params=params)
        response.raise_for_status()

        return Prompt.model_validate(response.json())

    async def get_prompt(self, prompt_id: str, prompt_version_id: str | None) -> Prompt:
        """
        Get a prompt version from storage, fetching from API if not found.
        """
        try:
            return await self.storage.get_prompt(prompt_id, prompt_version_id)
        except KeyError:
            # If not in storage, fetch from API and store
            prompt = await self.fetch_prompt(prompt_id, prompt_version_id)
            await self.storage.store_prompt(prompt)
            return prompt

    async def get_task(self, task_id: str, task_version_id: str | None) -> Task:
        """
        Get a task version from storage, fetching from API if not found.
        """
        try:
            return await self.storage.get_task(task_id, task_version_id)
        except KeyError:
            # If not in storage, fetch from API and store
            task = await self.fetch_task(task_id, task_version_id)
            await self.storage.store_task(task)
            return task

    async def fetch_prompt_schemas(
        self,
        prompt_id: str,
        version_id: str,
        schema_prompt_type: SchemaPromptType = SchemaPromptType.ALL,
    ) -> PromptSchemas:
        """
        Fetch schemas for a specific prompt version.
        Returns PromptSchemas containing SchemaWithMetadata objects.
        """
        params = {"version_id": version_id, "type": schema_prompt_type.value}

        response = await self.get(
            f"/prompts/{prompt_id}/schemas",
            params=params,
            headers=self.get_headers(),
        )

        if response.status_code == 404:
            raise KeyError(f"Prompt {prompt_id} or version {version_id} not found")

        response.raise_for_status()

        try:
            schemas = response.json()
            with open("temp.json", "w") as f:
                f.write(json.dumps(schemas, indent=2))

            # Pre-process schema data to handle self-references
            self._preprocess_schema_data(schemas)

            return PromptSchemas.model_validate(schemas)
        except Exception as e:
            logger.error(
                f"Error fetching prompt schemas for {prompt_id} version {version_id}: {e}",
                exc_info=True,
            )
            raise MoxnSchemaValidationError(
                prompt_id=prompt_id,
                version_id=version_id,
                schema=response.text,
                detail=str(e),
            )

    def _preprocess_schema_data(self, schema_data: dict) -> None:
        """
        Pre-process schema data to handle self-references and other validation issues.

        This method modifies the schema_data in place to ensure it can be properly
        validated by the Pydantic model.
        """
        # Process inputs
        if "inputs" in schema_data:
            for input_schema in schema_data["inputs"]:
                self._process_schema_properties(
                    input_schema.get("schema", {}).get("properties", [])
                )

        # Process outputs
        if "outputs" in schema_data:
            for output_schema in schema_data["outputs"]:
                self._process_schema_properties(
                    output_schema.get("schema", {}).get("properties", [])
                )

    def _process_schema_properties(self, properties: list) -> None:
        """
        Recursively process schema properties to fix validation issues.
        """
        if not properties:
            return

        for prop in properties:
            # Handle items property which might contain nested schema references
            if "items" in prop and isinstance(prop["items"], dict):
                # Process schemaRef if it exists
                if "schemaRef" in prop["items"] and isinstance(
                    prop["items"]["schemaRef"], dict
                ):
                    schema_ref = prop["items"]["schemaRef"]
                    # Convert boolean isSelfReference to string to match expected type
                    if "isSelfReference" in schema_ref and isinstance(
                        schema_ref["isSelfReference"], bool
                    ):
                        schema_ref["isSelfReference"] = str(
                            schema_ref["isSelfReference"]
                        ).lower()

                # Recursively process nested properties
                if "properties" in prop["items"] and isinstance(
                    prop["items"]["properties"], list
                ):
                    self._process_schema_properties(prop["items"]["properties"])

            # Process nested properties
            if "properties" in prop and isinstance(prop["properties"], list):
                self._process_schema_properties(prop["properties"])

            # Handle schemaRef at the property level
            if "schemaRef" in prop and isinstance(prop["schemaRef"], dict):
                schema_ref = prop["schemaRef"]
                if "isSelfReference" in schema_ref and isinstance(
                    schema_ref["isSelfReference"], bool
                ):
                    schema_ref["isSelfReference"] = str(
                        schema_ref["isSelfReference"]
                    ).lower()

    async def get_code_stubs(
        self,
        prompt_id: str,
        version_id: str,
        schema_prompt_type: SchemaPromptType = SchemaPromptType.ALL,
    ) -> CodegenResponse:
        try:
            params = {
                "version_id": version_id,
                "schema_type": schema_prompt_type.value,
            }

            response = await self.get(
                f"/prompts/{prompt_id}/codegen",
                params=params,
                headers=self.get_headers(),
                timeout=httpx.Timeout(30.0),
            )
            # Enhanced error handling
            if response.status_code != 200:
                logger.error(f"Codegen prompt failed: {response.status_code}")
                logger.error(f"Response content: {response.text}")

                try:
                    error_detail = response.json()
                    error_message = error_detail.get("detail", {}).get(
                        "message", response.text
                    )
                except json.JSONDecodeError:
                    error_message = response.text or f"HTTP {response.status_code}"

                raise RuntimeError(f"Codegen prompt failed: {error_message}")

            # Parse and validate response
            codegen_response = CodegenResponse.model_validate(response.json())
            logger.info(f"Generated {len(codegen_response.files)} files")
            return codegen_response
        except httpx.TimeoutException as e:
            logger.error(f"Prompt timed out: {e}")
            raise RuntimeError("Code stub prompt timed out") from e
        except Exception as e:
            logger.error(f"Code stub prompt failed: {e}", exc_info=True)
            raise RuntimeError("Code stub prompt failed") from e

    async def generate_code_stubs(
        self,
        prompt_id: str,
        version_id: str,
        schema_prompt_type: SchemaPromptType = SchemaPromptType.ALL,
        output_dir: Path | str | None = "./moxn_types",
    ) -> CodegenResponse:
        """
        Generate Python type stubs from prompt schemas.

        Args:
            prompt_id: The prompt ID
            version_id: The version ID
            schema_prompt_type: Type of schemas to generate (input, output, or all)
            output_dir: Optional directory to write the generated code to

        Returns:
            CodegenResponse object containing the generated code files

        Raises:
            MoxnSchemaValidationError: If schema validation fails
            RuntimeError: If the codegen prompt fails
            IOError: If file operations fail
        """
        logger.info(
            f"Generating code stubs for prompt {prompt_id} version {version_id}"
        )

        try:
            # Parse and validate response
            codegen_response = await self.get_code_stubs(
                prompt_id=prompt_id,
                version_id=version_id,
                schema_prompt_type=schema_prompt_type,
            )
            logger.info(f"Generated {len(codegen_response.files)} files")

            # Validate generated files
            for filename, content in codegen_response.files.items():
                logger.debug(f"Validating generated file: {filename}")
                if not content.strip():
                    raise ValueError(f"Generated code for {filename} is empty")
                if "class" not in content:
                    raise ValueError(
                        f"Generated code for {filename} doesn't contain a class definition"
                    )

            # Save files if configured
            if output_dir is not None:
                output_path = (
                    Path(output_dir) if isinstance(output_dir, str) else output_dir
                )
                output_path.mkdir(parents=True, exist_ok=True)

                for filename, content in codegen_response.files.items():
                    file_path = output_path / filename
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_text(content)
                    logger.info(f"Saved generated code to {file_path}")

            return codegen_response

        except httpx.TimeoutException as e:
            logger.error(f"Codegen prompt timed out: {e}")
            raise RuntimeError("Code generation timed out") from e
        except Exception as e:
            logger.error(f"Code generation failed: {e}", exc_info=True)
            raise

    async def create_telemetry_log(
        self,
        log_request: SpanLogRequest | SpanEventLogRequest,
    ) -> TelemetryLogResponse:
        """Send telemetry log to the API."""
        logger.debug(f"Sending telemetry log: {log_request}")

        try:
            # Ensure proper serialization of all fields
            json_data = log_request.model_dump(
                exclude_none=True,
                mode="json",
                by_alias=True,
            )

            response = await self.client.post(
                "/telemetry/log",
                json=json_data,
            )
            response.raise_for_status()

            return TelemetryLogResponse.model_validate(response.json())

        except httpx.TimeoutException as e:
            logger.error(f"Telemetry prompt timed out: {e}")
            raise RuntimeError("Telemetry prompt timed out") from e
        except Exception as e:
            logger.error(f"Telemetry prompt failed: {e}", exc_info=True)
            raise RuntimeError("Failed to send telemetry log") from e

    async def create_prompt_instance(
        self,
        prompt_id: str,
        version_id: str | None = None,
        input_schema: RenderableModel | None = None,
    ) -> PromptInstance:
        """
        Create a new PromptInstance for managing LLM interactions.

        Args:
            prompt_id: The base prompt ID
            version_id: Optional specific version
            input_schema: Optional input schema to use in message rendering
        """
        prompt = await self.get_prompt(prompt_id, version_id)
        return prompt.create_instance(input_schema=input_schema)

    async def prompt_instance_from_input_schema(
        self,
        input_schema: RenderableModel,
    ) -> PromptInstance:
        """
        Create a new PromptInstance for managing LLM interactions.

        Args:
            input_schema: Input schema to use in message rendering
        """
        prompt = await self.get_prompt(
            input_schema.model_version_config["metadata"].prompt_id,
            input_schema.model_version_config["metadata"].prompt_version_id,
        )
        return prompt.create_instance(input_schema=input_schema)

    @asynccontextmanager
    async def span(
        self,
        prompt_instance: PromptInstance,
        name: str | None = None,
        kind: Literal["llm", "tool", "agent"] = "llm",
        attributes: dict[str, Any] | None = None,
    ) -> AsyncGenerator[SpanContext, None]:
        """
        Creates a new span context and sets it as the current span.

        Example:
            async with client.span(name="agent_task", prompt_instance=prompt_instance, kind="agent"):
                # Do work within the span
                await client.log_telemetry_event(llm_event)
        """
        if name is None:
            name = prompt_instance.base_prompt.name
        async with self.telemetry_client.span(
            prompt_instance=prompt_instance,
            name=name,
            kind=kind,
            attributes=attributes,
        ) as span_context:
            yield span_context

    async def log_telemetry_event(
        self,
        event: LLMEvent,
        span_id: UUID | None = None,
    ) -> None:
        """
        Logs an LLM interaction event within the current span.

        Args:
            event: The LLM event to log
            span_id: Optional specific span ID to log to (uses current span if None)
        """
        await self.telemetry_client.log_event(event=event, span_id=span_id)

    async def send_telemetry_log_event_and_get_signed_url(
        self, signed_url_request: SignedUrlRequest
    ) -> SignedUrlResponse:
        """Send telemetry log and get a signed URL for uploading large data."""
        logger.debug(
            f"Sending telemetry log and getting signed URL: {signed_url_request}"
        )

        try:
            # Ensure proper serialization of all fields
            json_data = signed_url_request.model_dump(
                exclude_none=True,
                mode="json",
                by_alias=True,
            )

            response = await self.client.post(
                "/telemetry/log-event-signed-url",
                json=json_data,
            )
            response.raise_for_status()

            return SignedUrlResponse.model_validate(response.json())

        except httpx.TimeoutException as e:
            logger.error(f"Signed URL request timed out: {e}")
            raise RuntimeError("Telemetry signed URL request timed out") from e
        except Exception as e:
            logger.error(f"Signed URL request failed: {e}", exc_info=True)
            raise RuntimeError("Failed to get signed URL for telemetry data") from e

    async def flush(self, timeout: float | None = None) -> None:
        """
        Await in-flight telemetry logs (call this at process-exit,
        lambda return, or FASTAPI shutdown).
        """
        if timeout is None:
            timeout = self.settings.timeout
        await self.telemetry_client._dispatcher.flush(timeout)
