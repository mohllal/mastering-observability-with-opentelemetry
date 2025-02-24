# Stage 1 - Build the OpenTelemetry JS library
FROM node:18-slim AS opentelemetry-lib

WORKDIR /opentelemetry

RUN apt-get update \ 
  && apt-get install -y build-essential gcc git libpq-dev libsnappy-dev python3-dev \
  && rm -rf /var/lib/apt/lists/*

COPY _opentelemetry-js/package*.json ./
RUN npm install

COPY _opentelemetry-js ./

# Stage 2 - Build the service
FROM node:18-slim

WORKDIR /app

RUN apt-get update \ 
  && apt-get install -y build-essential gcc git libpq-dev libsnappy-dev python3-dev \
  && rm -rf /var/lib/apt/lists/*

COPY node-service-blue/package*.json ./
RUN npm install

COPY node-service-blue/ ./

# Copy the OpenTelemetry library with its node_modules
COPY --from=opentelemetry-lib /opentelemetry /app/_opentelemetry-js/
COPY --from=opentelemetry-lib /opentelemetry/node_modules /app/_opentelemetry-js/node_modules/

EXPOSE 3010

CMD ["npm", "start"]
