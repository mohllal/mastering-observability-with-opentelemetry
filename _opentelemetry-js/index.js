const { NodeSDK } = require("@opentelemetry/sdk-node");
const { getNodeAutoInstrumentations } = require("@opentelemetry/auto-instrumentations-node");
const { Resource } = require("@opentelemetry/resources");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-proto");
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
module.exports = (serviceName, serviceVersion) => {
  const otlpEndpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4318/v1/traces';

  // Create SDK configuration
  const sdk = new NodeSDK({
    resource: new Resource({
      [SEMRESATTRS_SERVICE_NAME]: serviceName,
      [SEMRESATTRS_SERVICE_VERSION]: serviceVersion
    }),
    traceExporter: new OTLPTraceExporter({ url: otlpEndpoint }),
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
