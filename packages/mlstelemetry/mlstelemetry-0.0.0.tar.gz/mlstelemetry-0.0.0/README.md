# MLSysOps Python Telemetry Library

Install with pip:
```
opentelemetry-exporter-otlp
opentelemetry-api
opentelemetry-sdk
```

And then the mlstelemetry library with the following command line:
```bash
python -m pip install mlstelemetry
```

If you want to use a requirements.txt :
```
mlstelemetry
opentelemetry-exporter-otlp
opentelemetry-api
opentelemetry-sdk

```
and then ```python -m pip -r requirements.txt```

### Usage

```
from mlstelemetry import MLSTelemetry

mlsTelemetryClient = MLSTelemetry("application_name", "application_component")


# async counter
mlsTelemetryClient.pushMetric(f'mls_python_asynccounter',"async_counter",intValue)
# counter
mlsTelemetryClient.pushMetric(f'mls_python_counter',"counter",floatValue)
# Gauge
mlsTelemetryClient.pushMetric(f'mls_python_test_gauge',"gauge",floatValue)
# Log
mlsTelemetryClient.pushLogInfo("MLSPythonTest Info Message",{"customAttribute": 2})
mlsTelemetryClient.pushLogDebug("MLSPythonTest Debug Message",{"customAttribute": 2})
mlsTelemetryClient.pushLogError("MLSPythonTest Error Message",{"customAttribute": 2})

```

### Environmental variables

Before starting the python script (or the container), we need to set the following environmental variable:

```TELEMETRY_ENDPOINT=<OTEL_COLLECTOR_IP:OTEL_COLLECTOR_PORT>```


If we need to configure how often it pushes data to the OTEL Collector, we need to set:

```EXPORT_INTERVAL=<value_in_ms>``` (Default: 1000ms)

The mode of aggregation is: average

This library can connect to Grafana to query data from two different data sources: Prometheus and Loki. 

The following environmental variables are used for configuration:

- **GRAFANA_ENDPOINT**: Specifies the address and port of the Grafana server used to make queries.
**Default:** `localhost:3000`
- **GRAFANA_API_KEY**: Provides the API key used for authentication when making requests to the Grafana server. Use a secure API key, especially in production environments.
**Default:** `"null"`
- **PROMETHEUS_DATASOURCE_ID**: Identifies the Prometheus datasource configured within Grafana. This ID is used when executing queries against Prometheus.
**Default:** `"null"`
- **LOKI_DATASOURCE_ID**: Identifies the Loki datasource configured within Grafana. This ID is used when querying log data from Loki.
**Default:** `"null"`


### Local OpenTelemetry Collector

For development purposes, you can start an OpenTelemetry Collector Docker container to see what is sent to the telemetry stream.

OpenTelemetry collector needs a configuration file to be provided. 

* Create a file named ```otelconfig.yaml```.
* Put the following configuration in the file:

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317

exporters:
  file:
    path: /logs/otelcol.log
  debug:
    verbosity: detailed

service:
  pipelines:
    metrics:
      receivers: [otlp]
      exporters: [file,debug]
    logs:
      receivers: [otlp]
      exporters: [file,debug]
```

And then you can start the OpenTelemetry Collector container with the following command:

```docker run --rm -p 4317:4317 -v "$PWD/otelconfig.yaml:/otelconfig.yaml" -v "$PWD/logs:/logs" otel/opentelemetry-collector-contrib --config /otelconfig.yaml```

Please notice that the configuration configures a file exporter, where it dumps every telemetry data to a logfile (in the ./logs directory). 

# How to fetch data from the local OTEL Collector

Use `get_metric_value_with_label` method, that retrieves specific metric values from a metrics dictionary. It allows filtering by:
- **Metric name** (required)
- **Node name** (optional)
- **Label name and label value** (optional).

This function is useful for pinpointing metrics based on certain attributes (e.g., `label_name` and `label_value`).

---

## Parameters

The method accepts the following parameters:

- **`metric_name`** (*required*):  
  The name of the metric you wish to retrieve.

- **`node_name`** (*optional*):  
  Filters the metrics based on the `key_service_hostname` label. If an empty string (`""`) is provided, this parameter is ignored.

- **`label_name`** (*optional*):  
  The specific label key to filter metrics (e.g., `"region"` or `"environment"`).

- **`label_value`** (*optional*):  
  The expected value for the given `label_name`.

---

## Return Value

- **Matching Metrics**:  
  A list of metric objects is returned when the specified filters match the metrics in the dictionary.

- **`None`**:  
  If no metrics match the filtering criteria, the method returns `None`.

---

## Usage Examples

### Example 1: Retrieve All Metrics for a Given Name
If you only want to retrieve all metrics for a specific `metric_name` without additional filters:

```python
result = get_metric_value_with_label(metric_name="cpu_usage")
print(result)
```

### Example 2: Filter by Node Name
To retrieve metrics for a specific `node_name`:

```python
result = get_metric_value_with_label(metric_name="cpu_usage", node_name="node123")
print(result)
```

### Example 3: Filter by Label Name and Value
To retrieve metrics filtered by a label, specify the `label_name` and `label_value`:

```python
result = get_metric_value_with_label(
    metric_name="cpu_usage",
    label_name="region",
    label_value="us-west"
)
print(result)
```

### Example 4: Combine Node Name and Label Filtering
You can also use both `node_name` and label filtering together as:

```python
result = get_local_value_with_label(
    metric_name="memory_usage",
    node_name="node456",
    label_name="environment",
    label_value="production"
)
print(result)
```

---

## Key Notes

1. **Empty Values**:  
   - If `node_name` is empty (`""`), the method skips filtering by `key_service_hostname`.
   - If either `label_name` or `label_value` is omitted, label-based filtering is skipped.

2. **Fallback Behavior**:  
   If no specific `node_name` or `label_name/label_value` filters are provided, the method retrieves all metrics matching the given `metric_name`.

3. **Error Handling**:  
   Ensure all inputs are valid (e.g., `metric_name` exists in the metrics dictionary) to avoid unexpected results.

4. **Empty hostname**:  
   If the metrics have not be enriched with label `key_service_hostname`, and `node_name` filter is used, it returns None.
---

# Using Log and Metric Receivers with `MLSTelemetry`

The `MLSTelemetry` client allows you to subscribe to **logs** and **metrics**, enabling real-time processing of telemetry data. This guide explains how to set up and use *log receivers* and *metric receivers* in your application.

---

## 1. Using the Log Receiver

The `subscribeToLocalLogs` method allows you to subscribe to log messages and process them using a custom handler.

### **Steps to Use the Log Receiver**

1. **Define a Log Handler Function**:  
   This function processes each received log. It takes the log message as an argument and performs your desired actions.

   Example:
   ```python
   def log_receive_handler(log):
       print(f"Received log: {log}")
   ```

2. **Subscribe to Logs**:  
   Use the `subscribeToLocalLogs` function of `mlsClient` to subscribe a handler that will be invoked every time a new log is received.

   Example:
   ```python
   await mlsClient.subscribeToLocalLogs(log_receive_handler)
   ```

3. **Start Listening for Logs**:  
   Use an asynchronous function to continuously listen for logs and subscribe handlers.

   Example:
   ```python
   async def log_listen():
       await asyncio.gather(
           mlsClient.subscribeToLocalLogs(log_receive_handler),
           mlsClient.subscribeToLocalLogs(log_receive_handler2)  # Optional additional handler
       )
   asyncio.run(log_listen())
   ```

### **Practical Use Case**
- Multiple handlers can be subscribed to the receiver to process logs in different ways, such as filtering, storing, or forwarding them to external systems.

---

## 2. Using the Metric Receiver

The `subscribeToMetrics` method allows you to subscribe and process telemetry metrics. With OpenTelemetry, this can include interactive tracing using spans.

### **Steps to Use the Metric Receiver**

1. **Define a Metric Handler Function**:  
   This function processes metrics as they are received. If tracing (`mlsClient.trace_enabled`) is enabled, you can attach spans to observe metric processing in detail.

   Example:
   ```python
   from opentelemetry.trace import SpanKind

   def metric_receive_handler(metric):
       if mlsClient.trace_enabled:
           with mlsClient.tracer.start_as_current_span("metrics_receiver",
                                                       context=metric["span_context"],
                                                       kind=SpanKind.SERVER) as span:
               print(f"Received metric with span: {metric['span_context']}")
       else:
           print(f"Received metric: {metric}")
   ```

2. **Subscribe to Metrics**:  
   Use the `subscribeToMetrics` function to subscribe a handler function to handle incoming metrics.

   Example:
   ```python
   await mlsClient.subscribeToMetrics(metric_receive_handler)
   ```

3. **Start Listening for Metrics**:  
   Use an asynchronous function to continuously receive metrics.

   Example:
   ```python
   async def metric_listen():
       await mlsClient.subscribeToMetrics(metric_receive_handler)
   asyncio.run(metric_listen())
   ```

### **Practical Use Case**
- Metric receivers can process real-time metrics for monitoring, alerting, and even debugging using OpenTelemetry spans for deeper observability.

---

## Example Output

Once the log and metric receivers are active, the output might look as follows:

- **Logs**:  
  A received log will be handled by the subscribed log handler and processed, for example:
  ```plaintext
  Received log: {"message": "Test log message", "level": "INFO", "timestamp": "..."}
  ```

- **Metrics**:  
  A received metric will be handled by the subscribed metric handler. If tracing is enabled, you might see:
  ```plaintext
  Received metric with span: {"span_id": "...", "trace_id": "..."}
  ```

---

## Additional Details

### Tracing Support
- If `mlsClient.trace_enabled` is `True`, OpenTelemetry spans are attached to metrics using the client’s `tracer`.
- These spans provide detailed traceability for metric processing operations.

### Key Methods
- **`subscribeToLocalLogs(handler_function)`**:  
  Subscribes a function (`handler_function`) that will handle log messages.

- **`subscribeToMetrics(handler_function)`**:  
  Subscribes a function (`handler_function`) that will process metrics as they are received.

### OTEL export configuration
You will also need to configure the OTEL to export to an OTLP endpoint, pointing to the client's IP:PORT
Set the enviromental variable:  
`METRIC_LISTENER_PORT=44318 (default)` for metrics  
`LOG_LISTENER_PORT=24317 (default` for logs
```yaml
  otlp/agentmetrics:
    endpoint: <AGENT IP>:<AGENT METRICS PORT>
    tls:
      insecure: true

  otlp/agentlogs:
    endpoint: <AGENT IP>:<AGENT LOGS PORT>
    tls:
      insecure: true
```
---

# How to Enable and Use Tracing in Your Application

Tracing provides valuable insight into the lifecycle of requests in your application. Follow the steps below to set up and use tracing effectively in your application, both for the **sending side** and the **receiving side**.

---

## Step 1: Enable Tracing via Environment Variable

Ensure that tracing is enabled in your application by setting the following environment variable:

```bash
export TELEMETRY_TRACE_ENABLED=on
```

This step ensures that tracing capabilities are activated in your environment.

---

## Step 2: Sending Tracing Data (Sender Side)

On the sending end, wrap the appropriate block of code using the `with` statement to establish a **tracing context**. Here’s how you can use the `mlsClient.tracer` to send traced metrics:

```python
from opentelemetry.trace import SpanKind

# Establish a tracing span for sending metrics
with mlsClient.tracer.start_as_current_span("test_span", kind=SpanKind.CLIENT):
    # Send a traced metric
    mlsClient.pushTracedMetric('mls_python_asynccounter', "gauge", 5)
```

### Key Points:
- Use `start_as_current_span` to start a tracing span.
- The `kind` parameter is set to `SpanKind.CLIENT`, indicating a client-side operation.
- Metrics are sent using the `pushTracedMetric` method within the tracing context.

---

## Step 3: Receiving Tracing Data (Receiver Side)

On the receiving end, usable only for **server mode**, you should also wrap the relevant code within a tracing context. Use the received span context (`metric['span_context']`) to maintain the current trace:

```python
from opentelemetry.trace import SpanKind

def receiving_callback_method(metric):
    # Establish a tracing span for receiving metrics
    with mlsClient.tracer.start_as_current_span("metrics_receiver",
                                                context=metric['span_context'],
                                                kind=SpanKind.SERVER) as span:
        # Handle the traced metric
        print(f'Received metric with span {metric['span_context']}')
```

### Key Points:
- Use `context=metric['span_context']` to propagate the received span context for the trace.
- The `kind` parameter is set to `SpanKind.SERVER`, indicating server-side trace handling.
- This pattern is specifically designed for server-based handling, not for pull-based methods.

---

