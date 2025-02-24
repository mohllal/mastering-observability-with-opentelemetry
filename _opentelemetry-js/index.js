const { initInstrumentation } = require("./instrumentation");
const { initResourceMetrics } = require("./metrics");

module.exports = {
  initInstrumentation,
  initResourceMetrics,
};
