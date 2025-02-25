from opentelemetry_py import init_instrumentation, init_resource_metrics


def start_instrumentation(app):
    """Start the OpenTelemetry instrumentation"""

    # initialize instrumentation
    flask_instrumentor = init_instrumentation("service-green", "1.0.0")
    flask_instrumentor.instrument_app(app)

    # setup resource metrics
    init_resource_metrics("service-green")
