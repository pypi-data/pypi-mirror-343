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

from datetime import datetime, timezone
import requests
import os
from prometheus_client.parser import text_string_to_metric_families

GRAFANA_ENDPOINT = os.getenv("GRAFANA_ENDPOINT","localhost:3000")
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY","null")
DATASOURCE_ID = os.getenv("PROMETHEUS_DATASOURCE_ID","null")

def unix_nano_to_rfc3339(nano_timestamp_str):
    """
    Converts a timestamp in nanoseconds since the Unix epoch to an RFC3339 formatted string.

    This function takes a string representation of a Unix timestamp in
    nanoseconds, converts it to seconds, formats it into a datetime object
    with UTC timezone, and then converts it to an RFC3339 formatted datetime
    string. It is useful for converting high-resolution timestamps to
    human-readable RFC3339 format.

    Arguments:
        nano_timestamp_str (str): The Unix timestamp in nanoseconds as a string.

    Returns:
        str: The RFC3339 formatted datetime string.
    """
    # Convert string to integer
    nano_timestamp = int(nano_timestamp_str)

    # Convert nanoseconds to seconds
    seconds_timestamp = nano_timestamp / 1_000_000_000

    # Convert seconds timestamp to datetime object
    dt = datetime.fromtimestamp(seconds_timestamp, tz=timezone.utc)

    # Format datetime object to RFC3339
    rfc3339_format = dt.isoformat()

    return rfc3339_format

def prometheus_query_range(query,start_time,end_time,step="10s",multiple=False,extra_columns=[]):
    """
    Queries Prometheus via Grafana server for a specific range of time-series data.

    This function performs a query to a Prometheus instance through Grafana to
    retrieve time-series data within a given range. The query can be configured
    with additional customization for step intervals, multiple results handling,
    and extra columns.

    Arguments:
        query: str
            The PromQL query to be executed for data retrieval.
        start_time: int
            Start of the time range to query, represented as a Unix timestamp in nano-
            seconds.
        end_time: int
            End of the time range to query, represented as a Unix timestamp in nano-
            seconds.
        step: str
            Duration string representing the query step interval (e.g., '10s', '1m'),
            with a default value of "10s".
        multiple: bool
            Indicates whether to handle multiple results for given queries. Defaults
            to False.
        extra_columns: list
            List of extra column names to be considered in the response data. Defaults
            to an empty list.

    Returns:
        dict
            A dictionary representing the time-series data retrieved for the requested
            query if successfully retrieved.

    Raises:
        None
    """
    # Define the Grafana server URL and API key
    grafana_url = f"http://{GRAFANA_ENDPOINT}/api/datasources/proxy/uid/{DATASOURCE_ID}/api/v1/query_range"

    # Construct the headers and query parameters
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_KEY}"
    }
    params = {
        "query": query,
        "start": unix_nano_to_rfc3339(start_time),
        "end": unix_nano_to_rfc3339(end_time),
        "step": step
    }
    # Send the request to Grafana
    response = requests.get(grafana_url, headers=headers, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the results
        return data['data']

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []

def prometheus_query(query,step="10s",multiple=False,extra_columns=[]):
    """
    Executes a Prometheus query via a Grafana datasource and returns the query results.

    This function sends a GET request to the Grafana API with the provided query and
    optional additional parameters. It retrieves and parses the JSON response, returning
    the resulting data from Prometheus. If the request fails, it prints the error information
    and returns an empty list instead.

    Parameters:
        query (str): The PromQL query string to execute.
        step (str, optional): The time interval between data points in the query. Defaults to "10s".
        multiple (bool, optional): Flag to indicate whether processing of multiple results is required.
            Defaults to False.
        extra_columns (list, optional): List of additional columns or data fields to consider in the
            query if applicable. Defaults to an empty list.

    Returns:
        dict: A dictionary containing the parsed results of the Prometheus query if successful.
        list: An empty list if the request fails.
    """
    # Define the Grafana server URL and API key
    grafana_url = f"http://{GRAFANA_ENDPOINT}/api/datasources/proxy/uid/{DATASOURCE_ID}/api/v1/query"

    # Construct the headers and query parameters
    headers = {
        "Authorization": f"Bearer {GRAFANA_API_KEY}"
    }
    params = {
        "query": query,
        "step": step
    }
    # Send the request to Grafana
    response = requests.get(grafana_url, headers=headers, params=params)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the results
        return data['data']

    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return []


def fetch_prometheus_metrics(url):
    """
    Fetch metrics from a Prometheus endpoint and parse them into a dictionary format.

    This function retrieves Prometheus metrics from the specified URL, processes the
    metric families, and organizes the collected data into a dictionary where the
    keys are metric names and the values are lists of corresponding data points.

    Args:
        url (str): The URL of the Prometheus endpoint to fetch metrics from.

    Returns:
        dict: A dictionary where keys are metric names (str), and values are lists of
        dictionaries containing 'labels' (dict), 'value' (float), and 'timestamp'
        (int or None).

    Raises:
        Exception: If the status code of the HTTP response is not 200.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching metrics: {response.status_code}")

    metrics_data = response.text
    metrics_dict = {}
    for family in text_string_to_metric_families(metrics_data):
        for sample in family.samples:
            metric_name = sample.name
            if metric_name not in metrics_dict:
                metrics_dict[metric_name] = []
            metrics_dict[metric_name].append({
                'labels': sample.labels,
                'value': sample.value,
                'timestamp': sample.timestamp,
            })

    return metrics_dict