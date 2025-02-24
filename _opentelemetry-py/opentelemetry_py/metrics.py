import os
import psutil
from opentelemetry import metrics
from opentelemetry.metrics import Observation

def get_cpu_usage(options):
    """
    Get the current CPU usage percentage.

    This function uses the psutil library to measure the CPU usage percentage
    over a 1-second interval and returns it as a list containing a single
    Observation object.
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    return [Observation(value=cpu_percent)]


def get_memory_usage(options):
    """
    Retrieves the current memory usage in bytes.

    This function uses the `psutil` library to obtain the system's virtual memory
    usage and returns it as a list containing a single `Observation` object with
    the memory usage in bytes.
    """
    memory = psutil.virtual_memory()
    return [Observation(value=memory.used)]


def format_service_name(service_name):
    """
    Format the service name to be used as a resource attribute.

    This function takes a service name as input and formats it to be used as a
    resource attribute by replacing spaces with underscores and converting the
    name to lowercase.
    """
    return service_name.replace(" ", "_").lower()


def init_resource_metrics(service_name):
    """
    Setup CPU and Memory usage metrics for the given service.

    This function creates two observable gauges for CPU and memory usage metrics
    using the provided service name. The CPU usage gauge observes the `get_cpu_usage`
    function, while the memory usage gauge observes the `get_memory_usage` function.
    """

    formatted_service_name = format_service_name(service_name)

    # Get meter from provider
    meter = metrics.get_meter(formatted_service_name)

    # Create observable gauges
    cpu_gauge = meter.create_observable_gauge(
        name=f"{formatted_service_name}.system.cpu.usage",
        description="CPU usage in percentage",
        unit="%",
        callbacks=[get_cpu_usage]
    )

    memory_gauge = meter.create_observable_gauge(
        name=f"{formatted_service_name}.system.memory.usage",
        description="Memory usage in bytes",
        unit="By",
        callbacks=[get_memory_usage]
    )

    return [cpu_gauge, memory_gauge]
