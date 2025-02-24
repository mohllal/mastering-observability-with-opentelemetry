const { NodeSDK } = require("@opentelemetry/sdk-node");
const { getNodeAutoInstrumentations } = require("@opentelemetry/auto-instrumentations-node");
const { Resource } = require("@opentelemetry/resources");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-proto");
const { OTLPMetricExporter } = require('@opentelemetry/exporter-metrics-otlp-proto');
const { PeriodicExportingMetricReader } = require('@opentelemetry/sdk-metrics');
const {
  SEMRESATTRS_SERVICE_NAME,
  SEMRESATTRS_SERVICE_VERSION,
} = require("@opentelemetry/semantic-conventions");

/**
 * Configure and initialize OpenTelemetry SDK
 * @param {string} serviceName - Name of the service to be monitored
 * @param {string} serviceVersion - Version of the service
 * @returns {NodeSDK} Configured OpenTelemetry SDK instance
 */
function initInstrumentation(serviceName, serviceVersion) {
  const otlpUrl = process.env.OTEL_EXPORTER_OTLP_URL || 'http://localhost:4318';

  const resource = new Resource({
    [SEMRESATTRS_SERVICE_NAME]: serviceName,
    [SEMRESATTRS_SERVICE_VERSION]: serviceVersion
  });

  const traceExporter = new OTLPTraceExporter({ url: `${otlpUrl}/v1/traces` });
  const metricExporter = new OTLPMetricExporter({ url: `${otlpUrl}/v1/metrics` });

  const metricReader = new PeriodicExportingMetricReader({
    exporter: metricExporter,
    exportIntervalMillis: 1000,
  });

  // Create SDK configuration
  const sdk = new NodeSDK({
    resource: resource,
    traceExporter: traceExporter,
    metricReader: metricReader,
    instrumentations: [
      getNodeAutoInstrumentations({
        "@opentelemetry/instrumentation-fs": { enabled: false },
      })
    ]
  });

  // Start the SDK
  sdk.start();
  return sdk;
};

module.exports = { initInstrumentation };