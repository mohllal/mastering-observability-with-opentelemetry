const logger = require('../config/logger');
const pkg = require('../package.json');
const { initInstrumentation, initResourceMetrics } = require("@local/opentelemetry-js");

function startInstrumentation() {
  logger.info("Starting OpenTelemetry instrumentation...")

  initInstrumentation(pkg.name, pkg.version);
  initResourceMetrics(pkg.name);
};

module.exports = startInstrumentation;