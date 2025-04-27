from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict
from .base import Monitor, Event, Metric, EventType, MetricType

class InMemoryMonitor(Monitor):
    """In-memory implementation of monitoring system"""
    
    def __init__(self):
        self._events: List[Event] = []
        self._metrics: List[Metric] = []
        self._metric_values: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    
    def record_event(self, event: Event) -> None:
        """Record an event
        
        Args:
            event: Event to record
        """
        self._events.append(event)
    
    def record_metric(self, metric: Metric) -> None:
        """Record a metric
        
        Args:
            metric: Metric to record
        """
        self._metrics.append(metric)
        
        # Update current value based on metric type
        metric_key = self._get_metric_key(metric.name, metric.labels)
        
        if metric.type == MetricType.COUNTER:
            self._metric_values[metric.name][metric_key] += metric.value
        elif metric.type == MetricType.GAUGE:
            self._metric_values[metric.name][metric_key] = metric.value
        elif metric.type in (MetricType.HISTOGRAM, MetricType.SUMMARY):
            # For histograms and summaries, we just store the raw values
            # In a real implementation, these would be aggregated properly
            self._metrics.append(metric)
    
    def get_events(self, 
                  session_id: Optional[str] = None,
                  agent_id: Optional[str] = None,
                  event_type: Optional[EventType] = None,
                  start_time: Optional[datetime] = None,
                  end_time: Optional[datetime] = None) -> List[Event]:
        """Get recorded events with optional filters
        
        Args:
            session_id: Filter by session ID
            agent_id: Filter by agent ID
            event_type: Filter by event type
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List of matching events
        """
        events = self._events
        
        if session_id:
            events = [e for e in events if e.session_id == session_id]
        if agent_id:
            events = [e for e in events if e.agent_id == agent_id]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        if start_time:
            events = [e for e in events if e.timestamp >= start_time]
        if end_time:
            events = [e for e in events if e.timestamp <= end_time]
            
        return sorted(events, key=lambda x: x.timestamp)
    
    def get_metrics(self,
                   metric_name: Optional[str] = None,
                   metric_type: Optional[MetricType] = None,
                   labels: Optional[Dict[str, str]] = None,
                   start_time: Optional[datetime] = None,
                   end_time: Optional[datetime] = None) -> List[Metric]:
        """Get recorded metrics with optional filters
        
        Args:
            metric_name: Filter by metric name
            metric_type: Filter by metric type
            labels: Filter by metric labels
            start_time: Filter by start time
            end_time: Filter by end time
            
        Returns:
            List of matching metrics
        """
        metrics = self._metrics
        
        if metric_name:
            metrics = [m for m in metrics if m.name == metric_name]
        if metric_type:
            metrics = [m for m in metrics if m.type == metric_type]
        if labels:
            metrics = [m for m in metrics if all(m.labels.get(k) == v for k, v in labels.items())]
        if start_time:
            metrics = [m for m in metrics if m.timestamp >= start_time]
        if end_time:
            metrics = [m for m in metrics if m.timestamp <= end_time]
            
        return sorted(metrics, key=lambda x: x.timestamp)
    
    def get_current_value(self, metric_name: str, labels: Optional[Dict[str, str]] = None) -> float:
        """Get current value of a metric
        
        Args:
            metric_name: Name of the metric
            labels: Optional metric labels
            
        Returns:
            Current value of the metric
        """
        metric_key = self._get_metric_key(metric_name, labels or {})
        return self._metric_values[metric_name][metric_key]
    
    def _get_metric_key(self, name: str, labels: Dict[str, str]) -> str:
        """Generate a unique key for a metric based on name and labels
        
        Args:
            name: Metric name
            labels: Metric labels
            
        Returns:
            Unique metric key
        """
        if not labels:
            return name
        
        # Sort labels to ensure consistent key generation
        sorted_labels = sorted(labels.items())
        label_str = ','.join(f"{k}={v}" for k, v in sorted_labels)
        return f"{name}[{label_str}]" 