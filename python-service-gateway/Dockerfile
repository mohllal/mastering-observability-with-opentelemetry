# Stage 1 - Build the OpenTelemetry Python library
FROM python:3.9-slim AS opentelemetry-lib

WORKDIR /opentelemetry

COPY _opentelemetry-py/requirements.txt .
COPY _opentelemetry-py/setup.py .
COPY _opentelemetry-py/opentelemetry_py ./opentelemetry_py

RUN pip install --no-cache-dir -r requirements.txt && \
  pip install --no-cache-dir -e .

# Stage 2 - Build the service
FROM python:3.9-slim

WORKDIR /app

COPY python-service-gateway/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the OpenTelemetry library and its dependencies
COPY --from=opentelemetry-lib /opentelemetry /app/_opentelemetry-py
COPY --from=opentelemetry-lib /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Set PYTHONPATH to include the local package
ENV PYTHONPATH=/app/_opentelemetry-py:${PYTHONPATH}

COPY python-service-gateway/ ./

EXPOSE 5000

CMD ["python", "app.py"]
