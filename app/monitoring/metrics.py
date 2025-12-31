"""
Metrics Collection for Taj Chat

Collects and exposes metrics for monitoring.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict
import threading


@dataclass
class MetricPoint:
    """Single metric data point."""
    name: str
    value: float
    timestamp: float
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class CounterMetric:
    """Counter metric that only increases."""
    value: float = 0.0
    created_at: float = field(default_factory=time.time)

    def inc(self, amount: float = 1.0):
        self.value += amount

    def get(self) -> float:
        return self.value


@dataclass
class GaugeMetric:
    """Gauge metric that can go up or down."""
    value: float = 0.0
    created_at: float = field(default_factory=time.time)

    def set(self, value: float):
        self.value = value

    def inc(self, amount: float = 1.0):
        self.value += amount

    def dec(self, amount: float = 1.0):
        self.value -= amount

    def get(self) -> float:
        return self.value


@dataclass
class HistogramMetric:
    """Histogram metric for distributions."""
    values: List[float] = field(default_factory=list)
    count: int = 0
    sum: float = 0.0
    buckets: Dict[float, int] = field(default_factory=lambda: {
        0.005: 0, 0.01: 0, 0.025: 0, 0.05: 0, 0.1: 0,
        0.25: 0, 0.5: 0, 1.0: 0, 2.5: 0, 5.0: 0, 10.0: 0,
    })
    created_at: float = field(default_factory=time.time)

    def observe(self, value: float):
        self.values.append(value)
        self.count += 1
        self.sum += value

        for bucket in sorted(self.buckets.keys()):
            if value <= bucket:
                self.buckets[bucket] += 1

    def get_percentile(self, p: float) -> float:
        if not self.values:
            return 0.0
        sorted_values = sorted(self.values)
        index = int(len(sorted_values) * p / 100)
        return sorted_values[min(index, len(sorted_values) - 1)]


class MetricsCollector:
    """
    Centralized metrics collection system.

    Collects:
    - Request counts and latencies
    - Agent execution metrics
    - Workflow statistics
    - Resource utilization
    - Error rates
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._counters: Dict[str, CounterMetric] = {}
        self._gauges: Dict[str, GaugeMetric] = {}
        self._histograms: Dict[str, HistogramMetric] = {}
        self._start_time = time.time()

        # Initialize default metrics
        self._init_default_metrics()

    def _init_default_metrics(self):
        """Initialize default metrics."""
        # Request metrics
        self.counter("http_requests_total", "Total HTTP requests")
        self.counter("http_errors_total", "Total HTTP errors")
        self.histogram("http_request_duration_seconds", "HTTP request duration")

        # Agent metrics
        self.counter("agent_tasks_total", "Total agent tasks")
        self.counter("agent_tasks_success", "Successful agent tasks")
        self.counter("agent_tasks_failed", "Failed agent tasks")
        self.histogram("agent_task_duration_seconds", "Agent task duration")

        # Workflow metrics
        self.counter("workflows_total", "Total workflows")
        self.counter("workflows_completed", "Completed workflows")
        self.counter("workflows_failed", "Failed workflows")
        self.histogram("workflow_duration_seconds", "Workflow duration")

        # Video metrics
        self.counter("videos_generated_total", "Total videos generated")
        self.gauge("videos_in_progress", "Videos currently being generated")

        # Resource metrics
        self.gauge("active_connections", "Active connections")
        self.gauge("memory_usage_bytes", "Memory usage in bytes")

    def counter(self, name: str, description: str = "") -> CounterMetric:
        """Get or create a counter metric."""
        with self._lock:
            if name not in self._counters:
                self._counters[name] = CounterMetric()
            return self._counters[name]

    def gauge(self, name: str, description: str = "") -> GaugeMetric:
        """Get or create a gauge metric."""
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = GaugeMetric()
            return self._gauges[name]

    def histogram(self, name: str, description: str = "") -> HistogramMetric:
        """Get or create a histogram metric."""
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = HistogramMetric()
            return self._histograms[name]

    def inc_counter(self, name: str, amount: float = 1.0, labels: Dict[str, str] = None):
        """Increment a counter."""
        key = self._make_key(name, labels)
        self.counter(key).inc(amount)

    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Set a gauge value."""
        key = self._make_key(name, labels)
        self.gauge(key).set(value)

    def observe_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Observe a histogram value."""
        key = self._make_key(name, labels)
        self.histogram(key).observe(value)

    def _make_key(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        """Create a unique key for a metric with labels."""
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def get_all_metrics(self) -> Dict:
        """Get all metrics as a dictionary."""
        with self._lock:
            return {
                "uptime_seconds": time.time() - self._start_time,
                "counters": {k: v.get() for k, v in self._counters.items()},
                "gauges": {k: v.get() for k, v in self._gauges.items()},
                "histograms": {
                    k: {
                        "count": v.count,
                        "sum": v.sum,
                        "avg": v.sum / v.count if v.count > 0 else 0,
                        "p50": v.get_percentile(50),
                        "p95": v.get_percentile(95),
                        "p99": v.get_percentile(99),
                    }
                    for k, v in self._histograms.items()
                },
            }

    def get_prometheus_metrics(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []
        lines.append(f"# HELP uptime_seconds Time since server start")
        lines.append(f"# TYPE uptime_seconds gauge")
        lines.append(f"uptime_seconds {time.time() - self._start_time}")

        with self._lock:
            for name, counter in self._counters.items():
                lines.append(f"# TYPE {name} counter")
                lines.append(f"{name} {counter.get()}")

            for name, gauge in self._gauges.items():
                lines.append(f"# TYPE {name} gauge")
                lines.append(f"{name} {gauge.get()}")

            for name, hist in self._histograms.items():
                lines.append(f"# TYPE {name} histogram")
                lines.append(f"{name}_count {hist.count}")
                lines.append(f"{name}_sum {hist.sum}")
                for bucket, count in sorted(hist.buckets.items()):
                    lines.append(f'{name}_bucket{{le="{bucket}"}} {count}')
                lines.append(f'{name}_bucket{{le="+Inf"}} {hist.count}')

        return "\n".join(lines)

    def reset(self):
        """Reset all metrics."""
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()
            self._start_time = time.time()
            self._init_default_metrics()


# Global metrics instance
metrics = MetricsCollector()
