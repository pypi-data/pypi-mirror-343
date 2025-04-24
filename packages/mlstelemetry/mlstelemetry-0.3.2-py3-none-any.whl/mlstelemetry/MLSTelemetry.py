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

import asyncio
import math
import socket
from typing import Iterable
import os
import sys
import time

from .MetricsReceiver import MetricsReceiver
from .PrometheusWrapper import prometheus_query,prometheus_query_range,fetch_prometheus_metrics
from .LokiWrapper import LogReceiver,fetch_logs
from cachetools import TTLCache, cached

# Metrics
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider, Counter, ObservableGauge
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter  import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import (PeriodicExportingMetricReader, AggregationTemporality)
from opentelemetry.metrics import CallbackOptions, Observation

# Span
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.trace import get_tracer
from opentelemetry.propagate import inject
from opentelemetry.trace import SpanKind

# Logs
from opentelemetry._logs import set_logger_provider
from opentelemetry._logs import get_logger
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics.view import LastValueAggregation

import logging

cache = TTLCache(maxsize=10000, ttl=1)

temporality_cumulative = {Counter: AggregationTemporality.CUMULATIVE}
temporality_delta = {Counter: AggregationTemporality.DELTA}
aggregation_last_value = {Counter: LastValueAggregation()}


# Now create a gauge instrument to make measurements with
def create_placement_gauge(signal):
    # Async Gauge
    def observable_gauge_func(options):
        yield metrics.Observation(signal.get_current_value(), {"component_id": signal.attribute})
    simple_gauge = meter.create_observable_gauge("component_placement_"+signal.attribute, [observable_gauge_func])
    return simple_gauge

class Signal:
    def __init__(self, attribute):
        self.attribute = attribute

    def set_current_value(self, i):
        self.current_value = i

    def get_current_value(self):
        return self.current_value



class MLSTelemetry:
    def __init__(self, application_name = "default", application_component = "none"):
        self.name = application_name
        self.instanceId = application_component
        self.otelendpoint = os.getenv("TELEMETRY_ENDPOINT","localhost:4317")

        self.resource = Resource(attributes={
            "service.name": self.name,
            "service.instance.id": self.instanceId,
            "service.hostname": socket.gethostname()}
        )
        self.log_receiver = None
        self.metrics_receiver = None
        self.__initMetrics()
        self.__initTracer()
        self.__initLogger()
        self.counters = {}
        self.trace_enabled = os.getenv("TELEMETRY_TRACE_ENABLED","off").lower() == "on"

        # Default attributes added to every instrument
        self.default_attributes = {
            "service.hostname": socket.gethostname()
        }

    def __del__(self):
        self.logger_provider.shutdown()

    def __initMetrics(self):
        readers = []

        metric_exporter = OTLPMetricExporter(
            # optional
            preferred_aggregation=aggregation_last_value,
            preferred_temporality=temporality_delta,
            endpoint=self.otelendpoint,
            insecure=True,
            # credentials=ChannelCredentials(credentials),
        )
        reader = PeriodicExportingMetricReader(
            exporter=metric_exporter,
            export_interval_millis=90,
        )
        readers.append(reader)

        provider = MeterProvider(metric_readers=readers,resource=self.resource)
        metrics.set_meter_provider(provider)


    def __initLogger(self):
        self.logger_provider = LoggerProvider(
            resource=self.resource
        )
        set_logger_provider(self.logger_provider)

        exporter = OTLPLogExporter(endpoint=self.otelendpoint,insecure=True)

        self.logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
        self.handler = LoggingHandler(level=logging.NOTSET, logger_provider=self.logger_provider)
        self.logger = logging.getLogger(self.name)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO) # TODO maybe need something else



    def __initTracer(self):
        # Configure trace provider
        trace.set_tracer_provider(TracerProvider(resource=self.resource))
        otlp_trace_exporter = OTLPSpanExporter(endpoint=os.getenv("MLS_TRACE_ENDPOINT",self.otelendpoint), insecure=True)

        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
        self.tracer = trace.get_tracer(self.name)

    def create_counter(self, name, instrument_type):
        """
        Creates and returns an instrument object based on the provided
        instrument type and name. The method checks the `instrument_type`
        against a predefined set of instrument classes and returns an
        instance of the corresponding class initialized with the given
        `name`. If the `instrument_type` is not recognized, it raises a
        ValueError indicating that the instrument type is unknown.

        :param name: The name assigned to the instrument.
        :type name: str
        :param instrument_type: The type of instrument to be created.
                                Accepted values are 'async_counter', 'counter',
                                or 'gauge'.
        :type instrument_type: str
        :return: An instance of the instrument corresponding to the specified
                 type, initialized with the given name.
        :rtype: MLSObservableCounter, MLSCounter, MLSGauge
        :raises ValueError: If the `instrument_type` is not recognized.
        """
        instrument_classes = {
            'async_counter': MLSObservableCounter,
            'counter': MLSCounter,
            'gauge': MLSGauge
        }

        if instrument_type in instrument_classes:
            return instrument_classes[instrument_type](name)
        else:
            raise ValueError(f"Unknown instrument type: {instrument_type}")


    def pushMetric(self,name,instrument_type,value,
                   description = "",frequency = 1, attributes = {},unit = ""):
        """
        Pushes a metric to the internal counters for tracking and monitoring purposes.

        This function allows you to submit a metric, identified by its name, and store
        or update it within an internal dictionary of counters. The metric consists of
        various components including an instrument type, value, description, frequency,
        additional attributes, and a unit of measurement. You can create new metrics or
        update existing ones. The proper functioning of this method enables effective
        metric analysis and observation.

        :param name:
            The name of the metric being pushed to the internal counters.
        :type name:
            str
        :param instrument_type:
            The type of instrument associated with the metric. It defines the nature
            or category of the measurement, such as a counter, gauge, etc.
        :type instrument_type:
            str
        :param value:
            The numeric value of the metric to be recorded. This represents the actual
            data point or measurement.
        :type value:
            float
        :param description:
            Optional description of the metric providing additional information
            about its purpose or usage.
        :type description:
            str, optional
        :param frequency:
            The frequency at which this metric is collected or updated, defaulting
            to 1 if not specified.
        :type frequency:
            int, optional
        :param attributes:
            Additional attributes related to the metric specified as a string, which
            may include key-value pairs or other descriptive data.
        :type attributes:
            str, optional
        :param unit:
            The unit of measurement for the metric, providing context for the metric
            value such as 'seconds', 'bytes', etc.
        :type unit:
            str, optional
        :return:
            None
        """
        if name not in self.counters:
            self.counters[name] = self.create_counter(name, instrument_type)
        attributes.update(self.default_attributes)
        self.counters[name].setValue(value,attributes)

    def pushTracedMetric(self,name,instrument_type,value,
                   description = "",frequency = 1, attributes = {},unit = ""):
        """
        Record a metric with a traceable context. This function creates a counter
        for the metric if it does not already exist and records the value by
        setting it. The metric is associated with a tracing span which helps
        with distributed tracing for monitoring and debugging purposes.

        :param name:
            The name of the metric to be recorded.
        :param instrument_type:
            Type of the instrument associated with the metric.
        :param value:
            The value of the metric to be set.
        :param description:
            An optional description of the metric.
        :param frequency:
            An optional frequency to specify how often the metric is recorded.
        :param attributes:
            Optional attributes providing additional context to the metric.
        :param unit:
            Optional unit of the metric value.

        :return:
            None
        """
        if name not in self.counters:
            self.counters[name] = self.create_counter(name, instrument_type)

        carrier = {}

        with trace.get_tracer(self.name).start_as_current_span(self.instanceId) as span:
            if span:
                span.set_attribute("service.name", self.name)

                # Inject the current span's trace context into the carrier
                inject(carrier)

                attributes.update(carrier)
            attributes.update(self.default_attributes)
            self.counters[name].setValue(value,attributes)

    def getMetric(self,name):
        pass

    def getHandler(self):
        return self.handler

    def pushLogInfo(self,message, attributes = {}):
        with trace.get_tracer(self.name).start_as_current_span(self.instanceId):
            self.logger.info(message)

    def _pushLogInfoAsync(self,message, attributes = {}):
        self.logger.info(message)

    async def pushLogInfoAsync(message,attributes = {}):
        # Simulate an async operation
        await asyncio.sleep(1)

    def pushLogDebug(self,message, attributes = {}):
        with trace.get_tracer(self.name).start_as_current_span(self.instanceId):
            self.logger.debug(message, extra=attributes)

    def pushLogError(self,message, attributes = {}):
        with trace.get_tracer(self.name).start_as_current_span(self.instanceId):
            self.logger.error(message)

    ### Get telemetry API
    @cached(cache)
    def getTelemetryLatest(self,metric_label= ""):
        '''
        Get the latest telemetry value in the system. Query telemetry from PromQL-compatible endpoint.
        :return:
        '''
        # result = prometheus_query(metric_label)
        result = fetch_prometheus_metrics("http://10.64.82.153:32769/metrics")

        return result

    def getTelemetryRange(self,metric_label,startTS,endTS):
        '''
        Get a telemetry metric between two timestamps.
        :param metric_label:
        :param startTS: Unix timestamp
        :param endTS:   Unix timestamp
        :return:
        '''

        result = prometheus_query_range(metric_label,startTS,endTS)

        return result

    def getLogs(self,filter):
        '''
        Get log messages given a string to filter the origin of the log messages.
        :param filter:
        :return:
        '''
        result = fetch_logs("test")

        return result

    @cached(cache)
    def getLocalMetrics(self,metric_label = ""):
        '''
        It always returns the latest readings, for the prometheus endpoint. It can query any prometheus endpoint.
        :param metric_label:
        :return:
        '''
        local_otel_agent_endpoint = os.getenv("LOCAL_OTEL_ENDPOINT", "localhost:9999")
        result = fetch_prometheus_metrics(local_otel_agent_endpoint)

        return result

    async def subscribeToLocalLogs(self,callback,topic):
        """
        :param callback: The callback function that will be executed when new logs are received.
        :param topic: The topic to subscribe to for receiving local logs.
        :return: None

        This method is used to subscribe to local logs. It creates a new LogReceiver instance if
        one is not already running, and then subscribes to the specified topic. If a LogReceiver is
        already running, it simply adds the callback function to the list of subscribers for the
        specified topic.
        """
        if self.log_receiver is None:
            self.log_receiver = LogReceiver(topic)
            serve_task = asyncio.create_task(self.log_receiver.serve())
            notify_task = asyncio.create_task(self.log_receiver.notify_subscribers())

            await asyncio.sleep(3)  # Adjust this duration if needed
            await asyncio.create_task(self.log_receiver.Subscribe(callback))
            await asyncio.gather(serve_task, notify_task)

        else:
            await self.log_receiver.Subscribe(callback)

    async def subscribeToMetrics(self, callback):
        """
        :param callback: A callback function that will be executed when new metrics are received.
        :param topic: The topic to subscribe to for receiving local metrics.
        :return: None

        This method is used to subscribe to metrics. If a MetricsReceiver instance is not
        already running, it creates a new one and begins serving. If a MetricsReceiver instance is
        already running, the callback is simply added to its subscriber list.
        """
        if self.metrics_receiver is None:
            self.metrics_receiver = MetricsReceiver(self.name)
            if self.trace_enabled:
                self.metrics_receiver.enable_tracing(self.tracer)
            serve_task = asyncio.create_task(self.metrics_receiver.serve())
            notify_task = asyncio.create_task(self.metrics_receiver.notify_subscribers())

            # Allow the server to initialize by adding a delay (adjust timeout if needed)
            await asyncio.create_task(self.metrics_receiver.Subscribe(callback))
            await asyncio.gather(serve_task, notify_task)

        else:
            await self.metrics_receiver.Subscribe(callback)

    def get_metric_value_with_label(self,agent="local",
                                    metric_name = "",
                                    label_name="", label_value = "",
                                    node_name = ""):
        """
        Fetches the value of a specified metric with specific label and label value, optionally
        filtered by the node name, from the collected metrics data. This method can retrieve
        metrics either from a local data source or from telemetry data depending on the
        provided `agent` parameter.

        :param agent: Specifies the source of metrics data. Use "local" for local metrics or other
                      values for telemetry data.
        :type agent: str
        :param metric_name: The name of the metric to retrieve.
        :type metric_name: str
        :param label_name: The name of the label to filter the metrics.
        :type label_name: str
        :param label_value: The value of the label to filter the metrics.
        :type label_value: str
        :param node_name: The name of the node to further filter the metric results. Defaults to
                          an empty string for no node filtering.
        :type node_name: str
        :return: Returns the metric data if available, filtered based on the parameters. Returns
                 None if the specified metric is not found or if no matching metrics are found
                 based on the filter criteria.
        :rtype: list[dict] or None
        """
        if agent == "local":
            metrics_dict = self.getLocalMetrics()
        else:
            metrics_dict = self.getTelemetryLatest()

        if metric_name in metrics_dict:
            if node_name == "":
                if label_name and label_value:
                    # Filter based on label_name and label_value
                    metric_result = [
                        metric for metric in metrics_dict[metric_name]
                        if metric["labels"].get(label_name) == label_value
                    ]
                    if len(metric_result) == 0:
                        return None
                    else:
                        return metric_result
                return metrics_dict[metric_name]
            else:
                metric_result = [
                    metric for metric in metrics_dict[metric_name]
                    if metric["labels"].get("key_service_hostname") == node_name
                ]
                if len(metric_result) == 0:
                    return None
                else:
                    if label_name and label_value:
                        # Additional filtering based on label_name and label_value
                        metric_result = [
                            metric for metric in metric_result
                            if metric["labels"].get(label_name) == label_value
                        ]
                        if len(metric_result) == 0:
                            return None
                    return metric_result

        return None



class MLSObservableCounter:
    """
    A class that represents an observable counter, designed to interact with a
    metrics meter and provide observations through a callback function. This
    class is used to track and report measurements over time, and is suitable
    for applications where monitoring and analysis of variable data is required.

    :ivar _name: The name of the observable counter, primarily used for
                 identification and logging purposes.
    :type _name: str
    :ivar _instance: The instance of the observable counter created via the
                     metrics library, containing the actual counter logic and
                     callback functionality.
    :type _instance: ObservableCounter
    :ivar _value: The current value of the observable counter, updated via the
                  setValue method and provided in the observations.
    :type _value: int
    """
    def __init__(self,name):
        self._name = name
        self._attributes = {}
        meter = metrics.get_meter(f'${name}_counter')

        self._instance = meter.create_observable_counter(
            name,
            callbacks=[self.counter_callback],
            description=f'${name} counter'
        )


    def counter_callback(self,options: CallbackOptions) -> Iterable[Observation]:
        observations = []
        if self._value is not None:
            observations.append(Observation(self._value, self._attributes))
            self._value = None
            self._attributes = None
        return observations

    def setValue(self, value,attributes):
        self._value = value
        self._attributes = attributes

class MLSCounter:

    def __init__(self,name):
        self._name = name
        meter = metrics.get_meter(f'${name}_counter')

        self._instance = meter.create_counter(
            name,
            description=f'${name} counter'
        )

    def setValue(self, value, attributes):
        self._value = value
        self._instance.add(value,attributes)

class MLSGauge:
    """
    Represents an MLS gauge, which is a tool for observing and monitoring
    specific metrics over time within a system. This class initializes
    an observable gauge using a meter and provides methods to set values
    and perform callback operations which supply observations for the gauge.

    :ivar _name: The name of the gauge, used for identification and metric
        categorization.
    :type _name: str
    :ivar _instance: The instance of the observable gauge created for
        this particular MLS gauge.
    :type _instance: ObservableGauge
    :ivar _value: The current value observed by the gauge.
    :type _value: Any
    """
    def __init__(self, name: str):
        self._name = name
        self._value = None
        self._attributes = {}

        meter = metrics.get_meter(f'${name}_gauge')
        self._instance = meter.create_observable_gauge(
            name,
            callbacks=[self.counter_callback],
            # unit="s",
            description=name + " gauge"
        )

    # Async Gauge
    def counter_callback(self,options: CallbackOptions) -> Iterable[Observation]:
        observations = []
        if self._value is not None:
            observations.append(Observation(self._value,self._attributes))
            self._value = None
            self._attributes = None
        return observations


    def setValue(self, value, attributes = {}):
        self._value = value
        self._attributes = attributes