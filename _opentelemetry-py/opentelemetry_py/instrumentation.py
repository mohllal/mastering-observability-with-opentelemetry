import os

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry import metrics


def init_instrumentation(service_name: str, service_version: str):
    """Initialize OpenTelemetry with OTLP exporter to Jaeger."""

    resource = Resource.create(
        {"service.name": service_name, "service.version": service_version}
    )

    init_traces_exporter(resource)
    init_metrics_exporter(resource)

    # Initialize instrumentations
    RequestsInstrumentor().instrument()
    PymongoInstrumentor().instrument()
    return FlaskInstrumentor()


def init_traces_exporter(resource):
    """Initialize OpenTelemetry with OTLP traces exporter."""

    otlp_url = os.getenv("OTEL_EXPORTER_OTLP_URL", "http://localhost:4318")

    # Set up the trace provider with OTLP exporter
    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(endpoint=f"{otlp_url}/v1/traces")
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def init_metrics_exporter(resource):
    """Initialize OpenTelemetry with OTLP metrics exporter."""

    # Configure the OTLP exporter
    otlp_url = os.getenv("OTEL_EXPORTER_OTLP_URL", "http://localhost:4318")

    # Create the OTLP metric exporter
    metric_exporter = OTLPMetricExporter(endpoint=f"{otlp_url}/v1/metrics")

    # Create MetricReader with the exporter
    reader = PeriodicExportingMetricReader(
        exporter=metric_exporter, export_interval_millis=1000
    )

    # Create MeterProvider with the reader
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])

    # Set the global MeterProvider
    metrics.set_meter_provider(meter_provider)
