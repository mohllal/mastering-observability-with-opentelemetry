# Stage 1 - Build the OpenTelemetry JS library
FROM node:18-alpine AS opentelemetry-lib

WORKDIR /opentelemetry

COPY _opentelemetry-js/package*.json ./
RUN npm install

COPY _opentelemetry-js ./

# Stage 2 - Build the service
FROM node:18-alpine

WORKDIR /app

COPY node-frontend/package*.json ./
RUN npm install

COPY node-frontend/ ./

# Copy the OpenTelemetry library with its node_modules
COPY --from=opentelemetry-lib /opentelemetry /app/_opentelemetry-js/
COPY --from=opentelemetry-lib /opentelemetry/node_modules /app/_opentelemetry-js/node_modules/

EXPOSE 8080

CMD ["npm", "start"]
