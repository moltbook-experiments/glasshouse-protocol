"""
Performance monitoring for UAT simulation workloads.
Tracks execution times, success rates, API latencies, and resource usage.
"""

import time
import logging
import psutil
import threading
from typing import Dict, Any, List, Optional
from collections import defaultdict
from dataclasses import dataclass, field
from contextlib import contextmanager

from logger import log_simulation_event

logger = logging.getLogger(__name__)

@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    start_time: float = 0.0
    end_time: float = 0.0
    duration: float = 0.0
    api_calls: int = 0
    api_latencies: List[float] = field(default_factory=list)
    memory_usage: List[float] = field(default_factory=list)
    cpu_usage: List[float] = field(default_factory=list)
    errors: int = 0
    retries: int = 0
    success_rate: float = 0.0

class PerformanceMonitor:
    """Monitors performance metrics during simulation runs."""

    def __init__(self):
        self.metrics: Dict[str, PerformanceMetrics] = {}
        self.global_start_time = time.time()
        self.monitoring_active = False
        self.monitor_thread: Optional[threading.Thread] = None
        self._stop_monitoring = threading.Event()

    def start_scenario_monitoring(self, scenario_name: str):
        """Start monitoring a specific scenario."""
        if scenario_name not in self.metrics:
            self.metrics[scenario_name] = PerformanceMetrics()

        self.metrics[scenario_name].start_time = time.time()
        logger.info(f"Started performance monitoring for scenario: {scenario_name}")

    def end_scenario_monitoring(self, scenario_name: str, success: bool = True):
        """End monitoring a specific scenario."""
        if scenario_name in self.metrics:
            metrics = self.metrics[scenario_name]
            metrics.end_time = time.time()
            metrics.duration = metrics.end_time - metrics.start_time

            if metrics.api_calls > 0:
                metrics.success_rate = (metrics.api_calls - metrics.errors) / metrics.api_calls
            else:
                metrics.success_rate = 1.0 if success else 0.0

            log_simulation_event('performance_metrics', {
                'scenario': scenario_name,
                'duration': metrics.duration,
                'api_calls': metrics.api_calls,
                'avg_api_latency': sum(metrics.api_latencies) / len(metrics.api_latencies) if metrics.api_latencies else 0,
                'errors': metrics.errors,
                'retries': metrics.retries,
                'success_rate': metrics.success_rate,
                'peak_memory_mb': max(metrics.memory_usage) if metrics.memory_usage else 0,
                'avg_cpu_percent': sum(metrics.cpu_usage) / len(metrics.cpu_usage) if metrics.cpu_usage else 0
            })

            logger.info(f"Performance monitoring completed for {scenario_name}: {metrics.duration:.2f}s")

    def record_api_call(self, scenario_name: str, latency: float, success: bool = True):
        """Record an API call with its latency."""
        if scenario_name in self.metrics:
            metrics = self.metrics[scenario_name]
            metrics.api_calls += 1
            metrics.api_latencies.append(latency)

            if not success:
                metrics.errors += 1

    def record_retry(self, scenario_name: str):
        """Record a retry attempt."""
        if scenario_name in self.metrics:
            self.metrics[scenario_name].retries += 1

    def start_global_monitoring(self):
        """Start global system monitoring in a background thread."""
        if self.monitoring_active:
            return

        self.monitoring_active = True
        self._stop_monitoring.clear()
        self.monitor_thread = threading.Thread(target=self._monitor_system_resources, daemon=True)
        self.monitor_thread.start()
        logger.info("Global performance monitoring started")

    def stop_global_monitoring(self):
        """Stop global system monitoring."""
        if not self.monitoring_active:
            return

        self.monitoring_active = False
        self._stop_monitoring.set()

        if self.monitor_thread:
            self.monitor_thread.join(timeout=5.0)

        total_duration = time.time() - self.global_start_time
        log_simulation_event('global_performance_summary', {
            'total_duration': total_duration,
            'scenarios_run': len(self.metrics),
            'total_api_calls': sum(m.api_calls for m in self.metrics.values()),
            'total_errors': sum(m.errors for m in self.metrics.values()),
            'overall_success_rate': self._calculate_overall_success_rate()
        })

        logger.info("Global performance monitoring stopped")

    def _monitor_system_resources(self):
        """Background thread to monitor system resources."""
        while not self._stop_monitoring.is_set():
            try:
                # Record system metrics for all active scenarios
                memory_mb = psutil.virtual_memory().used / (1024 * 1024)
                cpu_percent = psutil.cpu_percent(interval=None)

                for scenario_name, metrics in self.metrics.items():
                    if metrics.start_time > 0 and metrics.end_time == 0:  # Active scenario
                        metrics.memory_usage.append(memory_mb)
                        metrics.cpu_usage.append(cpu_percent)

                time.sleep(1.0)  # Sample every second

            except Exception as e:
                logger.error(f"Error in system monitoring: {e}")
                break

    def _calculate_overall_success_rate(self) -> float:
        """Calculate overall success rate across all scenarios."""
        total_calls = sum(m.api_calls for m in self.metrics.values())
        total_errors = sum(m.errors for m in self.metrics.values())

        if total_calls == 0:
            return 1.0

        return (total_calls - total_errors) / total_calls

    def get_scenario_metrics(self, scenario_name: str) -> Optional[PerformanceMetrics]:
        """Get metrics for a specific scenario."""
        return self.metrics.get(scenario_name)

    def get_all_metrics(self) -> Dict[str, PerformanceMetrics]:
        """Get all performance metrics."""
        return self.metrics.copy()

    @contextmanager
    def monitor_scenario(self, scenario_name: str):
        """Context manager for monitoring a scenario."""
        self.start_scenario_monitoring(scenario_name)
        try:
            yield self
        finally:
            self.end_scenario_monitoring(scenario_name)

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    return performance_monitor