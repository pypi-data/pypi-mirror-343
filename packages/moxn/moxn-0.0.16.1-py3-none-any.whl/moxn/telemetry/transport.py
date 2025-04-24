import json
import httpx
from typing import Protocol

from moxn.base_models.telemetry import (
    MAX_INLINE_ATTRIBUTES_SIZE,
    SignedUrlRequest,
    SignedUrlResponse,
    SpanEventLogRequest,
    SpanLogRequest,
    TelemetryLogResponse,
)


class TelemetryTransportBackend(Protocol):
    """Protocol for the backend that handles actual sending of telemetry data"""

    async def create_telemetry_log(
        self, log_request: SpanLogRequest | SpanEventLogRequest
    ) -> TelemetryLogResponse: ...

    async def send_telemetry_log_and_get_signed_url(
        self, log_request: SignedUrlRequest
    ) -> SignedUrlResponse: ...


class APITelemetryTransport:
    """Transport that sends telemetry data to the Moxn API"""

    def __init__(self, backend: TelemetryTransportBackend):
        self.backend = backend

    async def send_log(
        self, log_request: SpanLogRequest | SpanEventLogRequest
    ) -> TelemetryLogResponse:
        """Send telemetry log to the API"""

        # Only handle external storage for event logs with large attributes
        if isinstance(
            log_request, SpanEventLogRequest
        ) and self._should_use_external_storage(log_request.attributes):
            return await self._send_log_with_external_attributes(log_request)

        # Standard flow for smaller payloads
        return await self.backend.create_telemetry_log(log_request)

    def _should_use_external_storage(self, attributes: dict) -> bool:
        """Determine if attributes should be stored externally based on size"""
        # Estimate size by JSON serializing
        try:
            serialized = json.dumps(attributes)
            return len(serialized) > MAX_INLINE_ATTRIBUTES_SIZE
        except (TypeError, ValueError):
            # If we can't serialize, assume it's complex/large
            return True

    async def _send_log_with_external_attributes(
        self, log_request: SpanEventLogRequest
    ) -> TelemetryLogResponse:
        """Handle large attributes by uploading them separately"""
        # Save the attributes before clearing them from the request
        attributes = log_request.attributes

        # Create a request for a signed URL
        signed_url_request = SignedUrlRequest(
            file_path=f"telemetry/{log_request.span_id}/{log_request.span_event_id}/attributes.json",
            content_type="application/json",
            log_request=log_request,
        )

        # Get the signed URL
        signed_url_response = await self.backend.send_telemetry_log_and_get_signed_url(
            signed_url_request
        )

        # Create a modified request with empty attributes but add a reference
        # to where the attributes are stored
        modified_request = log_request.model_copy(deep=True)
        modified_request.attributes = {}
        modified_request.attributes_key = signed_url_response.file_path

        # Upload the attributes to the signed URL using httpx

        async with httpx.AsyncClient() as client:
            response = await client.put(
                signed_url_response.url,
                content=json.dumps(attributes),
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

        # Now send the event log without the large attributes
        return await self.backend.create_telemetry_log(modified_request)

    async def send_telemetry_log_and_get_signed_url(
        self, log_request: SignedUrlRequest
    ) -> SignedUrlResponse:
        """Send telemetry log and get a signed URL for uploading large data"""
        return await self.backend.send_telemetry_log_and_get_signed_url(log_request)
