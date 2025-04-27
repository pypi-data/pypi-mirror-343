from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MetricType(Enum):
    """Types of metrics that can be collected"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class EventType(Enum):
    """Types of events that can be tracked"""
    AGENT_START = "agent_start"
    AGENT_COMPLETE = "agent_complete"
    AGENT_ERROR = "agent_error"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    SERVICE_CALL = "service_call"
    SERVICE_RESULT = "service_result"

@dataclass
class Event:
    """Event data structure"""
    event_type: EventType
    timestamp: datetime
    session_id: str
    agent_id: Optional[str] = None
    tool_id: Optional[str] = None
    service_id: Optional[str] = None
    duration_ms: Optional[float] = None
    status: Optional[str] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None

@dataclass
class Metric:
    """Metric data structure"""
    name: str
    type: MetricType
    value: float
    timestamp: datetime
    labels: Dict[str, str]
    description: Optional[str] = None

class Monitor(ABC):
    """Base class for monitoring implementations"""
    
    @abstractmethod
    def record_event(self, event: Event) -> None:
        """Record an event
        
        Args:
            event: Event to record
        """
        pass
    
    @abstractmethod
    def record_metric(self, metric: Metric) -> None:
        """Record a metric
        
        Args:
            metric: Metric to record
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
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
        pass

class MonitoredMixin:
    """Mixin class to add monitoring capabilities to any class"""
    
    def __init__(self, monitor: Monitor):
        self.monitor = monitor
    
    def record_event(self, event: Event) -> None:
        """Record an event using the monitor
        
        Args:
            event: Event to record
        """
        self.monitor.record_event(event)
    
    def record_metric(self, metric: Metric) -> None:
        """Record a metric using the monitor
        
        Args:
            metric: Metric to record
        """
        self.monitor.record_metric(metric) 