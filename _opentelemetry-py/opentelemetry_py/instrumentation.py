import os

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.pymongo import PymongoInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry._logs import set_logger_provider


DEFAULT_OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"


def init_instrumentation(service_name: str, service_version: str):
    """Initialize OpenTelemetry with OTLP exporter to Jaeger."""

    resource = Resource.create(
        {"service.name": service_name, "service.version": service_version}
    )

    init_traces_exporter(resource)
    init_metrics_exporter(resource)
    init_logs_exporter(resource)

    # Initialize instrumentations
    RequestsInstrumentor().instrument()
    PymongoInstrumentor().instrument()
    return FlaskInstrumentor()


def init_traces_exporter(resource):
    """Initialize OpenTelemetry with OTLP traces exporter."""

    otlp_url = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT", DEFAULT_OTEL_EXPORTER_OTLP_ENDPOINT
    )

    # Set up the trace provider with OTLP exporter
    provider = TracerProvider(resource=resource)
    otlp_exporter = OTLPSpanExporter(endpoint=f"{otlp_url}/v1/traces")
    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)


def init_metrics_exporter(resource):
    """Initialize OpenTelemetry with OTLP metrics exporter."""

    # Configure the OTLP exporter
    otlp_url = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT", DEFAULT_OTEL_EXPORTER_OTLP_ENDPOINT
    )

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


def init_logs_exporter(resource):
    """Initialize OpenTelemetry with OTLP logs exporter."""

    otlp_url = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT", DEFAULT_OTEL_EXPORTER_OTLP_ENDPOINT
    )

    # Create and set the logger provider
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)

    # Create the OTLP log exporter
    log_exporter = OTLPLogExporter(endpoint=f"{otlp_url}/v1/logs")

    # Create and add the log processor
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
