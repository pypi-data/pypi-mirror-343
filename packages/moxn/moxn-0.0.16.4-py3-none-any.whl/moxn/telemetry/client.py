from __future__ import annotations

from contextlib import asynccontextmanager
from contextvars import Token
from datetime import datetime, timezone
from typing import Any, AsyncGenerator, Literal, Optional
from uuid import UUID, uuid4

from moxn.base_models.telemetry import (
    LLMEvent,
    SpanLogRequest,
    SpanLogType,
    SpanKind,
)
from moxn.models.prompt import PromptInstance
from moxn.telemetry.backend import TelemetryTransportBackend
from moxn.telemetry.dispatcher import TelemetryDispatcher
from .context import SpanContext, current_span
import asyncio


class TelemetryClient:
    """
    Higher-level façade that tracks spans and delegates *sending* to a backend.
    """

    def __init__(self, backend: TelemetryTransportBackend) -> None:
        self._backend = backend
        # create and start the fire-and-forget dispatcher
        self._dispatcher = TelemetryDispatcher(backend)
        # schedule the background workers on the running loop
        asyncio.create_task(self._dispatcher.start())

    # --------------------------------------------------------------------- #
    # Span helpers (unchanged except for backend wiring)
    # --------------------------------------------------------------------- #

    @asynccontextmanager
    async def span(
        self,
        prompt_instance: PromptInstance,
        name: str | None = None,
        kind: Literal["llm", "tool", "agent"] | SpanKind = "llm",
        attributes: Optional[dict[str, Any]] = None,
    ) -> AsyncGenerator[SpanContext, None]:
        if isinstance(kind, str):
            kind = SpanKind(kind)

        parent_context = current_span.get()

        if name is None:
            name = prompt_instance.base_prompt.name

        context = (
            parent_context.create_child(name, kind, attributes)
            if parent_context
            else SpanContext.create_root(
                name=name,
                kind=kind,
                prompt_id=prompt_instance.prompt_id,
                prompt_version_id=prompt_instance.prompt_version_id,
                transport=self._dispatcher,
                attributes=attributes,
            )
        )

        await self._log_span_start(context)
        token: Token = current_span.set(context)

        try:
            yield context
        except Exception as exc:
            await self._log_span_error(context, str(exc))
            raise
        finally:
            current_span.reset(token)
            await self._log_span_end(context)

    async def log_event(self, event: LLMEvent, span_id: Optional[UUID] = None) -> None:
        context = current_span.get() if span_id is None else None
        if context is None:
            raise RuntimeError(
                f"No active span context found (span_id={span_id!s})"
            )  # pragma: no cover

        await context.log_event(
            message="LLM response received",
            metadata={"event_type": "llm_response"},
            attributes=event.model_dump(mode="json", by_alias=True),
        )

    # ------------------------------------------------------------------ #
    # Internal logging helpers (backend-aware)
    # ------------------------------------------------------------------ #

    async def _log_span_start(self, ctx: SpanContext) -> None:
        attrs = {"span.name": ctx.name, "span.kind": ctx.kind.value, **ctx.attributes}
        await self._dispatcher.enqueue(
            SpanLogRequest(
                id=uuid4(),
                timestamp=ctx.start_time,
                span_id=ctx.span_id,
                root_span_id=ctx.root_span_id,
                parent_span_id=ctx.parent_span_id,
                event_type=SpanLogType.START,
                prompt_id=ctx.prompt_id,
                prompt_version_id=ctx.prompt_version_id,
                attributes=attrs,
                message=f"Started span: {ctx.name}",
            )
        )

    async def _log_span_error(self, ctx: SpanContext, error_msg: str) -> None:
        await self._dispatcher.enqueue(
            SpanLogRequest(
                id=uuid4(),
                timestamp=datetime.now(timezone.utc),
                span_id=ctx.span_id,
                root_span_id=ctx.root_span_id,
                parent_span_id=ctx.parent_span_id,
                event_type=SpanLogType.ERROR,
                prompt_id=ctx.prompt_id,
                prompt_version_id=ctx.prompt_version_id,
                attributes=ctx.attributes,
                message=f"Error in span {ctx.name}: {error_msg}",
            )
        )

    async def _log_span_end(self, ctx: SpanContext) -> None:
        await self._dispatcher.enqueue(
            SpanLogRequest(
                id=uuid4(),
                timestamp=datetime.now(timezone.utc),
                span_id=ctx.span_id,
                root_span_id=ctx.root_span_id,
                parent_span_id=ctx.parent_span_id,
                event_type=SpanLogType.END,
                prompt_id=ctx.prompt_id,
                prompt_version_id=ctx.prompt_version_id,
                attributes=ctx.attributes,
                message=f"Completed span: {ctx.name}",
            )
        )

    async def aclose(self) -> None:
        """
        Flush & cancel workers, then close the HTTP clients in the backend.
        Call this on application shutdown to avoid leaked connections.
        """
        # this flushes + cancels + joins
        await self._dispatcher.stop()
        # now close the AsyncClient(s)
        if hasattr(self._backend, "aclose"):
            await self._backend.aclose()
