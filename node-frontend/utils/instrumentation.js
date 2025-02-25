const { initInstrumentation, initResourceMetrics } = require("@local/opentelemetry-js");

const pkg = require('../package.json');

initInstrumentation(pkg.name, pkg.version);
initResourceMetrics(pkg.name);