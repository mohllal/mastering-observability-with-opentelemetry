import os
from typing import Dict, Any, Tuple
import logging

import requests
from flask import Flask, request, jsonify
from opentelemetry_py import init_instrumentation, init_resource_metrics


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

SERVICE_CONFIG = {
    "blue": os.getenv("SERVICE_BLUE_URL", "http://localhost:3010"),
    "green": os.getenv("SERVICE_GREEN_URL", "http://localhost:3020"),
}


def start_instrumentation():
    """Start the OpenTelemetry instrumentation"""

    logger.info("Starting OpenTelemetry instrumentation...")

    # initialize instrumentation
    flask_instrumentor = init_instrumentation("service-gateway", "1.0.0")
    flask_instrumentor.instrument_app(app)

    # setup resource metrics
    init_resource_metrics("service-gateway")


start_instrumentation()


class LoadBalancer:
    """
    LoadBalancer class to manage routing requests between services.

    Attributes:
        request_count (int): Counter to keep track of the number of requests.
        threshold (int): Number of requests after which the service is switched.

    Methods:
        __init__():
            Initializes the LoadBalancer with a request count and threshold.

        get_target_service() -> str:
            Determines which service to route to based on the current request count.
            Returns:
                str: The name of the target service ("blue" or "green").
    """
    def __init__(self):
        self.request_count = 0
        self.threshold = 3  # Switch services after 3 requests

    def get_target_service(self) -> str:
        """Determine which service to route to based on request count"""
        current_service = "blue" if self.request_count < self.threshold else "green"
        self.request_count = (self.request_count + 1) % (self.threshold * 2)
        return current_service


load_balancer = LoadBalancer()


def forward_request(service: str, choice: str) -> Tuple[Dict[str, Any], int]:
    """Forward the request to the appropriate service"""

    url = f"{SERVICE_CONFIG[service]}?choice={choice}"

    try:
        response = requests.get(url, timeout=5)
        return response.json(), response.status_code
    except requests.RequestException as e:
        logger.error("Error forwarding request to %s service: %s", service, str(e))
        return {"error": f"Service unavailable: {str(e)}"}, 503


@app.route("/")
def index():
    choice = request.args.get("choice", "")
    target_service = load_balancer.get_target_service()

    logger.info("Forwarding request to %s service with choice: %s", target_service, choice)
    response_data, status_code = forward_request(target_service, choice)

    return jsonify(response_data), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
