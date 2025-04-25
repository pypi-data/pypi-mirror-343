"""Initialize Lilypad OpenTelemetry instrumentation."""

import logging
import importlib.util
from secrets import token_bytes
from collections.abc import Sequence

from pydantic import TypeAdapter
from opentelemetry import trace
from opentelemetry.trace import INVALID_SPAN_ID, INVALID_TRACE_ID
from opentelemetry.sdk.trace import IdGenerator, ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import (
    SpanExporter,
    SpanExportResult,
    BatchSpanProcessor,
)

from ._utils.client import get_sync_client
from ._utils.settings import get_settings
from ._utils.otel_debug import wrap_batch_processor
from ..types.projects.functions import SpanPublic

try:
    from rich.logging import RichHandler as LogHandler
except ImportError:
    from logging import StreamHandler as LogHandler

DEFAULT_LOG_LEVEL: int = logging.INFO

# Ignore pydantic deprecation warnings by using `list[SpanPublic]` instead of `TraceCreateResponse`
TraceCreateResponseAdapter = TypeAdapter(list[SpanPublic])


class CryptoIdGenerator(IdGenerator):
    """Generate span/trace IDs with cryptographically secure randomness."""

    def _random_int(self, n_bytes: int) -> int:
        return int.from_bytes(token_bytes(n_bytes), "big")

    def generate_span_id(self) -> int:
        span_id = self._random_int(8)  # 64bit
        while span_id == INVALID_SPAN_ID:
            span_id = self._random_int(8)
        return span_id

    def generate_trace_id(self) -> int:
        trace_id = self._random_int(16)  # 128bit
        while trace_id == INVALID_TRACE_ID:
            trace_id = self._random_int(16)
        return trace_id


class _JSONSpanExporter(SpanExporter):
    """A custom span exporter that sends spans to a custom endpoint as JSON."""

    def __init__(self) -> None:
        """Initialize the exporter with the custom endpoint URL."""
        self.settings = get_settings()
        self.client = get_sync_client(api_key=self.settings.api_key)
        self.log = logging.getLogger(__name__)

    def pretty_print_display_names(self, span: SpanPublic) -> None:
        """Extract and pretty print the display_name attribute from each span, handling nested spans."""
        settings = get_settings()
        self.log.info(
            f"View the trace at: {settings.remote_client_url}/projects/{settings.project_id}/traces/{span.uuid}"
        )
        self._print_span_node(span, indent=0)

    def _print_span_node(self, span: SpanPublic, indent: int) -> None:
        """Recursively print a SpanNode and its children with indentation."""
        indent_str = "    " * indent  # 4 spaces per indent level

        self.log.info(f"{indent_str}{span.display_name}")

        for child in span.child_spans:
            self._print_span_node(child, indent + 1)

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        """Convert spans to a list of JSON serializable dictionaries"""
        span_data = [self._span_to_dict(span) for span in spans]

        try:
            raw_response = self.client.projects.traces.create(
                project_uuid=self.settings.project_id, extra_body=span_data
            )
            response_spans = TraceCreateResponseAdapter.validate_python(raw_response)
            if len(response_spans) > 0:
                for response_span in response_spans:
                    self.pretty_print_display_names(response_span)
                return SpanExportResult.SUCCESS
            else:
                return SpanExportResult.FAILURE
        except Exception as e:
            self.log.error(f"Error sending spans: {e}")
            return SpanExportResult.FAILURE

    def _span_to_dict(self, span: ReadableSpan) -> dict:
        """Convert the span data to a dictionary that can be serialized to JSON"""
        # span.instrumentation_scope to_json does not work
        instrumentation_scope = (
            {
                "name": span.instrumentation_scope.name,
                "version": span.instrumentation_scope.version,
                "schema_url": span.instrumentation_scope.schema_url,
                "attributes": dict(span.instrumentation_scope.attributes.items())
                if span.instrumentation_scope.attributes
                else None,
            }
            if span.instrumentation_scope
            else {
                "name": None,
                "version": None,
                "schema_url": None,
                "attributes": {},
            }
        )
        return {
            "trace_id": f"{span.context.trace_id:032x}" if span.context else None,
            "span_id": f"{span.context.span_id:016x}" if span.context else None,
            "parent_span_id": f"{span.parent.span_id:016x}" if span.parent else None,
            "instrumentation_scope": instrumentation_scope,
            "resource": span.resource.to_json(0),
            "name": span.name,
            "start_time": span.start_time,
            "end_time": span.end_time,
            "attributes": dict(span.attributes.items()) if span.attributes else {},
            "status": span.status.status_code.name,
            "events": [
                {
                    "name": event.name,
                    "attributes": dict(event.attributes.items()) if event.attributes else {},
                    "timestamp": event.timestamp,
                }
                for event in span.events
            ],
            "links": [
                {
                    "context": {
                        "trace_id": f"{link.context.trace_id:032x}",
                        "span_id": f"{link.context.span_id:016x}",
                    },
                    "attributes": link.attributes,
                }
                for link in span.links
            ],
        }


def configure(
    *,
    log_level: int = DEFAULT_LOG_LEVEL,
    log_format: str | None = None,
    log_handlers: list[logging.Handler] | None = None,
    auto_llm: bool = False,
) -> None:
    """Initialize the OpenTelemetry instrumentation for Lilypad and configure log outputs.

    The user can configure log level, format, and output destination via the parameters.
    This allows adjusting log outputs for local runtimes or different environments.
    """
    # Configure logging for Lilypad.
    logger = logging.getLogger("lilypad")
    logger.setLevel(log_level)
    if not log_handlers:
        if log_handlers is None:
            log_handlers = []
        log_handlers.append(LogHandler())
    for log_handler in log_handlers:
        log_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(log_handler)

    # Proceed with tracer provider configuration.
    if trace.get_tracer_provider().__class__.__name__ == "TracerProvider":
        logger.error("TracerProvider already initialized.")  # noqa: T201
        return
    otlp_exporter = _JSONSpanExporter()
    provider = TracerProvider(id_generator=CryptoIdGenerator())
    processor = BatchSpanProcessor(otlp_exporter)  # pyright: ignore[reportArgumentType]
    if log_level == logging.DEBUG:
        wrap_batch_processor(processor)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    if not auto_llm:
        return

    if importlib.util.find_spec("openai") is not None:
        from lilypad.lib._opentelemetry import OpenAIInstrumentor

        OpenAIInstrumentor().instrument()
    if importlib.util.find_spec("anthropic") is not None:
        from lilypad.lib._opentelemetry import AnthropicInstrumentor

        AnthropicInstrumentor().instrument()
    if importlib.util.find_spec("azure") is not None and importlib.util.find_spec("azure.ai.inference") is not None:
        from lilypad.lib._opentelemetry import AzureInstrumentor

        AzureInstrumentor().instrument()
    if importlib.util.find_spec("google") is not None:
        if importlib.util.find_spec("google.genai") is not None:
            from lilypad.lib._opentelemetry import GoogleGenAIInstrumentor

            GoogleGenAIInstrumentor().instrument()
    if importlib.util.find_spec("botocore") is not None:
        from lilypad.lib._opentelemetry import BedrockInstrumentor

        BedrockInstrumentor().instrument()
    if importlib.util.find_spec("mistralai") is not None:
        from lilypad.lib._opentelemetry import MistralInstrumentor

        MistralInstrumentor().instrument()
    if importlib.util.find_spec("outlines") is not None:
        from lilypad.lib._opentelemetry import OutlinesInstrumentor

        OutlinesInstrumentor().instrument()
