#   Copyright (c) 2025. MLSysOps Consortium
#   #
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#   #
#       http://www.apache.org/licenses/LICENSE-2.0
#   #
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#  #
#  #

import os
import asyncio
import grpc
from opentelemetry.proto.collector.metrics.v1 import metrics_service_pb2_grpc
from opentelemetry.proto.collector.metrics.v1 import metrics_service_pb2
from opentelemetry.propagate import extract
from opentelemetry.trace import SpanKind


# Utility function to check attributes
def check_attribute(resource, key, value):
    """
    Check if a resource has the specified key-value attribute.
    """
    for item in resource.attributes:
        if item.key == key and item.value.string_value == value:
            return True
    return False

def get_attribute_by_key(data, string_key_name, field_type="string_value"):
    """
    Retrieves the value of a specific attribute by its key from a data structure.

    This method iterates through a collection of attributes (typically a `RepeatedCompositeContainer` from a protobuf structure)
    and searches for an attribute with the specified key. If the key is found, and the associated value has the specified type
    (e.g., string, int, etc.), it retrieves and returns that value. Otherwise, it returns `None`.

    Args:
        data (iterable):
            An iterable collection (such as a `RepeatedCompositeContainer`) containing attributes.
            Each attribute is expected to have a `key` field and a `value` field, where `value` could contain
            different types (e.g., string, int, bool, etc.).
        string_key_name (str):
            The key of the attribute whose value needs to be retrieved.
        field_type (str, optional):
            The type of the value associated with the key. This defaults to `"string_value"`
            (to retrieve string values). Other possible types include `"int_value"`, `"double_value"`, etc.

    Returns:
        object:
            The value of the attribute that matches the `string_key_name` and matches the specified `field_type`.
            Returns `None` if:
            - No attribute with the specified key exists in the data.
            - The matching attribute does not have a value with the specified type.
            - Malformed data is encountered.

    Raises:
        None:
            The method safely handles common exceptions such as `KeyError`, `IndexError`, and `TypeError`,
            and returns `None` if such exceptions occur. This ensures it doesn't throw errors for invalid or
            incomplete input data.

    Example:
        ```python
        from opentelemetry.proto.common.v1.common_pb2 import AnyValue, KeyValue

        # Create mock attributes as a list of KeyValue protobuf objects
        attributes = [
            KeyValue(key="host", value=AnyValue(string_value="localhost")),
            KeyValue(key="port", value=AnyValue(int_value=8080)),
        ]

        # Retrieve values by key
        host = get_attribute_by_key(attributes, "host")  # Output: "localhost"
        port = get_attribute_by_key(attributes, "port", field_type="int_value")  # Output: 8080
        invalid_key = get_attribute_by_key(attributes, "invalid_key")  # Output: None
        wrong_type = get_attribute_by_key(attributes, "host", field_type="int_value")  # Output: None
        ```
    """
    try:
        # Iterate through attributes and find the one matching the string_key_name
        for attr in data:
            if attr.key == string_key_name:
                # Return the string value for the matching key
                if attr.value.HasField(field_type):
                    return attr.value.string_value
        # Return None if no match is found
        return None
    except (KeyError, IndexError, TypeError):
        # Handle cases where the data structure is malformed or keys are missing
        return None

class MetricsReceiver(metrics_service_pb2_grpc.MetricsServiceServicer):
    def __init__(self, topic):
        self.subscribers = []
        self.metric_queue = asyncio.Queue()
        self.topic = topic
        self.trace_enabled = False
        self.tracer = None

    async def Subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def notify_subscribers(self):
        while True:
            metric_message = await self.metric_queue.get()
            for subscriber in self.subscribers:
                subscriber(metric_message)

    def enable_tracing(self, tracer):
        self.trace_enabled = True
        self.tracer = tracer

    def disable_tracing(self):
        self.trace_enabled = False
        self.tracer = None

    async def Export(self, request, context):
        """
        Export is called whenever metrics arrive. It processes the request
        and queues the metrics for further processing.
        """
        if self.trace_enabled:
            # Extract trace context from gRPC metadata
            metadata = context.invocation_metadata()  # gRPC metadata
            carrier = {item.key: item.value for item in metadata}  # Convert to a dictionary
            span_context = extract(carrier)  # Extract the context using OpenTelemetry propagator
            with self.tracer.start_as_current_span(self.topic,context=span_context, kind=SpanKind.SERVER) as span:
                span.add_event("Received metric.")

        try:
            for resource_metrics in request.resource_metrics:
                for scope_metrics in resource_metrics.scope_metrics:
                    for metric in scope_metrics.metrics:
                        # Check for the registered topic
                        metric_message = {
                            "name": metric.name,
                            "description": metric.description,
                            "unit": metric.unit,
                            "resource_attributes_raw": resource_metrics.resource.attributes,
                            "resource_attributes": {
                                "service.name": get_attribute_by_key(resource_metrics.resource.attributes, "service.name"),
                                "service.instance.id": get_attribute_by_key(resource_metrics.resource.attributes, "service.instance.id"),
                            },
                            "data": []
                        }

                        # Process metric data points based on type
                        if metric.HasField("gauge"):
                            for data_point in metric.gauge.data_points:
                                metric_message['data'].append({
                                    "timestamp": data_point.time_unix_nano,
                                    "value": data_point.as_double if data_point.HasField(
                                        "as_double") else data_point.as_int,
                                    "attributes": data_point.attributes,
                                })
                        elif metric.HasField("sum"):
                            for data_point in metric.sum.data_points:
                                metric_message['data'].append({
                                    "timestamp": data_point.time_unix_nano,
                                    "value": data_point.as_double if data_point.HasField(
                                        "as_double") else data_point.as_int,
                                    "attributes": data_point.attributes
                                })

                        elif metric.HasField("histogram"):
                            for data_point in metric.histogram.data_points:
                                metric_message['data'].append({
                                    "timestamp": data_point.time_unix_nano,
                                    "bucket_counts": data_point.bucket_counts,
                                    "sum": data_point.sum,
                                    "count": data_point.count,
                                    "attributes": data_point.attributes
                                })

                        elif metric.HasField("exponential_histogram"):
                            for data_point in metric.exponential_histogram.data_points:
                                metric_message['data'].append({
                                    "timestamp": data_point.time_unix_nano,
                                    "scale": data_point.scale,
                                    "sum": data_point.sum,
                                    "count": data_point.count,
                                    "attributes": data_point.attributes
                                })

                        elif metric.HasField("summary"):
                            for data_point in metric.summary.data_points:
                                metric_message['data'].append({
                                    "timestamp": data_point.time_unix_nano,
                                    "count": data_point.count,
                                    "sum": data_point.sum,
                                    "quantile_values": [
                                        {"quantile": qv.quantile, "value": qv.value}
                                        for qv in data_point.quantile_values
                                    ],
                                    "attributes": data_point.attributes
                                })

                        if self.trace_enabled:
                            traceparent = get_attribute_by_key(metric_message.get('data', [])[0]['attributes'], "traceparent")
                            metric_message['span_context'] = extract({"traceparent": traceparent})

                        # Add a processed metric message to the queue
                        await self.metric_queue.put(metric_message)
            return metrics_service_pb2.ExportMetricsServiceResponse()

        except AttributeError as e:
            print(f"AttributeError: {e}")
            return metrics_service_pb2.ExportMetricsServiceResponse()

    async def serve(self):
        """
        Start the gRPC server for receiving OTLP metrics.
        """
        server = grpc.aio.server()
        metrics_service_pb2_grpc.add_MetricsServiceServicer_to_server(self, server)
        localport = os.getenv("METRIC_LISTENER_PORT", "44318")
        server.add_insecure_port(f'[::]:{localport}')
        await server.start()
        print(f"OTLP Metrics Server is running on port {localport}")
        await server.wait_for_termination()
