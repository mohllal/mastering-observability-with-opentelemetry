const logsAPI = require('@opentelemetry/api-logs');

function formatLog(severity, message, attributes = {}) {
  const timestamp = new Date().toISOString();
  const attributesString = Object.keys(attributes).length ? JSON.stringify(attributes) : '';
  return `${timestamp} ${severity.padEnd(5)} ${message} ${attributesString}`;
}

function initLogger(name = 'logger') {
  const provider = logsAPI.logs.getLoggerProvider();
  const baseLogger = provider.getLogger(name);

  const createLogMethod = (level, severityNumber) => {
    return (message, attributes = {}) => {
      const timestamp = Date.now() * 1000000;
      const body = message instanceof Error ? message.stack || message.message : message;

      // Format attributes as key-value pairs for better Loki querying
      const logAttributes = {
        ...attributes,
        level,
        logger: name,
        error: message instanceof Error ? message.message : undefined
      };

      console[level.toLowerCase()](formatLog(level, body, attributes));

      baseLogger.emit({
        severityNumber,
        severityText: level,
        body,
        attributes: logAttributes,
        timestamp: timestamp
      });
    };
  };

  return {
    debug: createLogMethod('DEBUG', logsAPI.SeverityNumber.DEBUG),
    info: createLogMethod('INFO', logsAPI.SeverityNumber.INFO),
    warn: createLogMethod('WARN', logsAPI.SeverityNumber.WARN),
    error: createLogMethod('ERROR', logsAPI.SeverityNumber.ERROR)
  };
}

module.exports = { initLogger };
