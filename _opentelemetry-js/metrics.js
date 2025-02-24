const pidusage = require('pidusage');
const { metrics } = require('@opentelemetry/api');

function formatServiceName(serviceName) {
  return serviceName.replace(/\s+/g, '_').toLowerCase();
}

async function getCurrentStats() {
  const stats = await pidusage(process.pid);
  return stats;
};

/*
  * Setup resource metrics
  * @param {string} serviceName - The name of the service
  */

function initResourceMetrics(serviceName) {
  const formattedServiceName = formatServiceName(serviceName);

  const meter = metrics.getMeter(formattedServiceName);

  // CPU usage observable gauge
  const cpuGauge = meter.createObservableGauge(`${formattedServiceName}.system.cpu.usage`, {
    description: 'CPU usage in percentage',
    unit: '%'
  });

  // Memory usage observable gauge
  const memoryGauge = meter.createObservableGauge(`${formattedServiceName}.system.memory.usage`, {
    description: 'Memory usage in bytes',
    unit: 'By'
  });

  cpuGauge.addCallback(async (observableResult) => {
    const stats = await getCurrentStats();
    observableResult.observe(stats.cpu, {
      pid: process.pid.toString(),
      type: 'cpu'
    });
  });

  memoryGauge.addCallback(async (observableResult) => {
    const stats = await getCurrentStats();
    observableResult.observe(stats.memory, {
      pid: process.pid.toString(),
      type: 'memory'
    });
  });
}

module.exports = { initResourceMetrics };
