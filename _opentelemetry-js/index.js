const { initInstrumentation } = require("./instrumentation");
const { initResourceMetrics } = require("./metrics");
const { initLogger } = require("./logger");

module.exports = {
  initInstrumentation,
  initResourceMetrics,
  initLogger,
};
