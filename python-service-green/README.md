# Python Service Green

## Start Service with OTel Agent

```bash
opentelemetry-instrument --traces_exporter console --metrics_exporter none --logs_exporter none --service_name service-green flask run --port 3020
```

## Enable OTel Log Instrumentation

### Mac/Linux

```bash
export OTEL_PYTHON_LOG_CORRELATION=true
export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
```

### Windows

```bash
set OTEL_PYTHON_LOG_CORRELATION=true
set OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true
```
