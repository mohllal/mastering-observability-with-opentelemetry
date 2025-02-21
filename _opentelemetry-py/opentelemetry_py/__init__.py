from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor

def init_telemetry(service_name: str, service_version: str):
    """Initialize OpenTelemetry with the given service details."""

    resource = Resource.create({
        "service.name": service_name,
        "service.version": service_version
    })

    # Set up the trace provider
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Initialize instrumentations
    RequestsInstrumentor().instrument()
    PymongoInstrumentor().instrument()

    return FlaskInstrumentor()
