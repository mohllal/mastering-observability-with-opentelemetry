const pkg = require('../package.json');
const { trace } = require("@opentelemetry/api");

class SlowOperation {
  static async call(operationName, minDelay = 300, maxDelay = 1000) {
    const tracer = trace.getTracer(pkg.name, pkg.version);

    return tracer.startActiveSpan(`${operationName}`, async (span) => {
      try {
        // Generate random delay between min and max
        const delay = Math.floor(Math.random() * (maxDelay - minDelay + 1) + minDelay);

        span.setAttribute("operation.delay_ms", delay);

        // Simulate slow operation
        await new Promise(resolve => setTimeout(resolve, delay));

        span.end();
      } catch (error) {
        span.recordException(error);
        span.setStatus({ code: 2 }); // SpanStatusCode.ERROR
        span.end();
        throw error;
      }
    });
  }
}

module.exports = SlowOperation;
