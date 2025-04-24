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

import json
from datetime import datetime, timezone
import requests
import os
import asyncio
import grpc
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2_grpc
from opentelemetry.proto.collector.logs.v1 import logs_service_pb2

GRAFANA_ENDPOINT = os.getenv("GRAFANA_ENDPOINT","localhost:3000")
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY","null")
DATASOURCE_ID = os.getenv("LOKI_DATASOURCE_ID","null")


def check_attribute(resource, key, value):
    """
    Checks if a specific key-value pair is present in the attributes of a given resource.

    This function iterates through the list of attributes in the provided resource to determine
    if one of the attributes matches the given key and value.

    Args:
        resource: The resource object containing a list of attributes to check.
        key (str): The key to search for within the resource's attributes.
        value (str): The value to search for in combination with the specified key.

    Returns:
        bool: True if a matching key-value pair is found in the resource attributes,
        False otherwise.
    """
    for item in resource.attributes:
        if item.key == key and item.value.string_value == value:
            return True
    return False


def fetch_logs(query,start_time,end_time,step="10s"):
    """
    Fetches logs from a Grafana Loki data source for a specified query and time
    range.

    This function interacts with a Grafana Loki data source using its API to
    retrieve log data that matches the specified query. Results are returned
    for the specified start and end times, and the entries are parsed from the
    response. The log body and corresponding timestamp are extracted.

    Parameters:
        query : str
            The Loki query string for filtering logs.
        start_time : str
            The start time for the log query in nanoseconds since epoch.
        end_time : str
            The end time for the log query in nanoseconds since epoch.
        step : str, optional
            The interval step for the query range (default is "10s").

    Returns:
        dict
            A dictionary representing the first log entry found, structured as
            {"body": str, "timestamp": str}, or {"body": "", "timestamp": ""}
            if no logs are found or an error occurs.

    Raises:
        None
    """
    # Define the Grafana server URL and API key
    grafana_url = f"http://{GRAFANA_ENDPOINT}/grafana/api/datasources/proxy/uid/{DATASOURCE_ID}/loki/api/v1/query_range"

    # Construct the headers and query parameters
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_KEY}"
    }

    params = {
        "query": query,
        "start": start_time,
        "end": end_time,
        "step": step,
        "direction": "FORWARD"
    }

    # Send the request to Grafana
    response = requests.post(grafana_url, headers=headers, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        if data['status'] == 'success':
            log_values = data['data']['result'][0]['values']
            for log_entry in log_values:
                timestamp = log_entry[0]
                body = json.loads(log_entry[1])['body']

                print(f'{timestamp} : {body}')
                return {"body" : body, "timestamp": timestamp }
        return None

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return {"body" : "", "timestamp": "" }



class LogReceiver(logs_service_pb2_grpc.LogsServiceServicer):
    """
    Handles log processing and subscriber notification for the LogsService.

    This class is designed to facilitate the receipt, processing, and forwarding
    of log data to subscribers. It implements the LogsServiceServicer, handling
    incoming logs from gRPC clients, filtering them based on a configured topic,
    and dispatching them to registered subscribers.

    Attributes:
        subscribers (list): A list of subscriber functions to be notified of new logs.
        log_queue (Asyncio.Queue): An asynchronous queue to manage incoming log messages.
        topic (str): The topic used to filter logs for processing and notification.
    """
    def __init__(self,topic):
        self.subscribers = []
        self.log_queue = asyncio.Queue()
        self.topic = topic

    async def Subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    async def notify_subscribers(self):
        while True:
            log_message = await self.log_queue.get()
            for subscriber in self.subscribers:
                subscriber(log_message)

    async def Export(self, request, context):
        try:
            for resource_logs in request.resource_logs:
                for scope_logs in resource_logs.scope_logs:
                    for log_record in scope_logs.log_records:
                        # Check for registered topic
                        if check_attribute(resource_logs.resource,"service.name",self.topic):
                            log_message = {
                                "timestamp": log_record.time_unix_nano,
                                "body": log_record.body.string_value,
                                "attributes": resource_logs.resource.attributes,
                                "severity": log_record.severity_text
                            }
                            await self.log_queue.put(log_message)
            return logs_service_pb2.ExportLogsServiceResponse()
        except AttributeError as e:
            print(f"AttributeError: {e}")
            return logs_service_pb2.ExportLogsServiceResponse()

    async def serve(self):
        server = grpc.aio.server()
        logs_service_pb2_grpc.add_LogsServiceServicer_to_server(self, server)
        localport = os.getenv("LOG_LISTENER_PORT","24317")
        server.add_insecure_port(f'[::]:{localport}')
        await server.start()
        print(f"OTLP Log Server is running on port {localport}")
        await server.wait_for_termination()