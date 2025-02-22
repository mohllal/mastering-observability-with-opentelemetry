from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

def init_telemetry(service_name: str, service_version: str):
    """Initialize OpenTelemetry with OTLP exporter to Jaeger."""

    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version
    })

    # Set up the trace provider with OTLP exporter
    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(
        endpoint="http://jaeger:4318/v1/traces"
    )
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Initialize instrumentations
    RequestsInstrumentor().instrument()
    PymongoInstrumentor().instrument()

    return FlaskInstrumentor()
