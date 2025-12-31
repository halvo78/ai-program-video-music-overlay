"""
Performance Monitoring for Taj Chat

Tracks execution times, resource usage, and bottlenecks.
"""

import time
import asyncio
import psutil
import functools
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from contextlib import contextmanager, asynccontextmanager
import logging

from .metrics import metrics

logger = logging.getLogger(__name__)


@dataclass
class TimingRecord:
    """Record of a timed operation."""
    name: str
    duration_ms: float
    start_time: datetime
    end_time: datetime
    success: bool
    metadata: Dict = field(default_factory=dict)


class PerformanceMonitor:
    """
    Performance monitoring system.

    Features:
    - Function timing decorators
    - Context managers for timing
    - Resource usage tracking
    - Bottleneck detection
    - Performance reports
    """

    def __init__(self, max_records: int = 10000):
        self._records: List[TimingRecord] = []
        self._max_records = max_records
        self._start_time = time.time()

    @contextmanager
    def timer(self, name: str, metadata: Dict = None):
        """Context manager for timing operations."""
        start = time.time()
        start_dt = datetime.now()
        success = True

        try:
            yield
        except Exception:
            success = False
            raise
        finally:
            end = time.time()
            duration_ms = (end - start) * 1000

            record = TimingRecord(
                name=name,
                duration_ms=duration_ms,
                start_time=start_dt,
                end_time=datetime.now(),
                success=success,
                metadata=metadata or {},
            )

            self._add_record(record)

            # Update metrics
            metrics.observe_histogram(
                f"operation_duration_seconds",
                end - start,
                {"operation": name},
            )

    @asynccontextmanager
    async def async_timer(self, name: str, metadata: Dict = None):
        """Async context manager for timing operations."""
        start = time.time()
        start_dt = datetime.now()
        success = True

        try:
            yield
        except Exception:
            success = False
            raise
        finally:
            end = time.time()
            duration_ms = (end - start) * 1000

            record = TimingRecord(
                name=name,
                duration_ms=duration_ms,
                start_time=start_dt,
                end_time=datetime.now(),
                success=success,
                metadata=metadata or {},
            )

            self._add_record(record)

            metrics.observe_histogram(
                f"operation_duration_seconds",
                end - start,
                {"operation": name},
            )

    def timed(self, name: str = None):
        """Decorator for timing function execution."""
        def decorator(func: Callable) -> Callable:
            operation_name = name or func.__name__

            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                with self.timer(operation_name):
                    return func(*args, **kwargs)

            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                async with self.async_timer(operation_name):
                    return await func(*args, **kwargs)

            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            return sync_wrapper

        return decorator

    def _add_record(self, record: TimingRecord):
        """Add a timing record, removing old ones if needed."""
        self._records.append(record)

        if len(self._records) > self._max_records:
            self._records = self._records[-self._max_records // 2:]

    def get_stats(self, name: str = None) -> Dict:
        """Get statistics for operations."""
        records = self._records
        if name:
            records = [r for r in records if r.name == name]

        if not records:
            return {"count": 0}

        durations = [r.duration_ms for r in records]
        success_count = sum(1 for r in records if r.success)

        return {
            "count": len(records),
            "success_rate": success_count / len(records),
            "min_ms": min(durations),
            "max_ms": max(durations),
            "avg_ms": sum(durations) / len(durations),
            "p50_ms": sorted(durations)[len(durations) // 2],
            "p95_ms": sorted(durations)[int(len(durations) * 0.95)] if len(durations) > 1 else durations[0],
            "p99_ms": sorted(durations)[int(len(durations) * 0.99)] if len(durations) > 1 else durations[0],
        }

    def get_slow_operations(self, threshold_ms: float = 1000) -> List[TimingRecord]:
        """Get operations that exceeded the threshold."""
        return [r for r in self._records if r.duration_ms > threshold_ms]

    def get_resource_usage(self) -> Dict:
        """Get current resource usage."""
        process = psutil.Process()

        return {
            "cpu_percent": process.cpu_percent(),
            "memory_mb": process.memory_info().rss / 1024 / 1024,
            "memory_percent": process.memory_percent(),
            "threads": process.num_threads(),
            "open_files": len(process.open_files()),
            "connections": len(process.connections()),
        }

    def get_system_info(self) -> Dict:
        """Get system information."""
        return {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_total_gb": psutil.virtual_memory().total / 1024 / 1024 / 1024,
            "memory_available_gb": psutil.virtual_memory().available / 1024 / 1024 / 1024,
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage("/").percent,
        }

    def get_report(self) -> Dict:
        """Generate a comprehensive performance report."""
        # Group records by name
        by_name: Dict[str, List[TimingRecord]] = {}
        for record in self._records:
            if record.name not in by_name:
                by_name[record.name] = []
            by_name[record.name].append(record)

        operation_stats = {}
        for name, records in by_name.items():
            operation_stats[name] = self.get_stats(name)

        slow_ops = self.get_slow_operations()

        return {
            "generated_at": datetime.now().isoformat(),
            "uptime_seconds": time.time() - self._start_time,
            "total_operations": len(self._records),
            "unique_operations": len(by_name),
            "operation_stats": operation_stats,
            "slow_operations_count": len(slow_ops),
            "resource_usage": self.get_resource_usage(),
            "system_info": self.get_system_info(),
        }

    def reset(self):
        """Reset all performance data."""
        self._records.clear()
        self._start_time = time.time()


# Global performance monitor
performance_monitor = PerformanceMonitor()


# Convenience decorators
def timed(name: str = None):
    """Decorator for timing function execution."""
    return performance_monitor.timed(name)
