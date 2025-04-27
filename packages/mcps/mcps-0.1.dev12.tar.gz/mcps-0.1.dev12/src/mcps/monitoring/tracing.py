from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid
from .base import Monitor, Event, EventType

@dataclass
class Span:
    """Trace span representing a single operation"""
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "in_progress"  # in_progress, success, error
    error: Optional[str] = None
    tags: Dict[str, str] = None
    metadata: Dict[str, Any] = None

class Tracer:
    """Tracer for creating and managing trace spans"""
    
    def __init__(self, monitor: Monitor):
        self.monitor = monitor
        self._active_spans: Dict[str, Span] = {}
        self._current_span_id: Optional[str] = None
    
    def start_trace(self, name: str, tags: Optional[Dict[str, str]] = None) -> str:
        """Start a new trace
        
        Args:
            name: Name of the trace
            tags: Optional trace tags
            
        Returns:
            Trace ID
        """
        trace_id = str(uuid.uuid4())
        return self.start_span(name, trace_id=trace_id, tags=tags)
    
    def start_span(self, 
                  name: str, 
                  trace_id: Optional[str] = None,
                  parent_span_id: Optional[str] = None,
                  tags: Optional[Dict[str, str]] = None) -> str:
        """Start a new span
        
        Args:
            name: Name of the span
            trace_id: Optional trace ID (generated if not provided)
            parent_span_id: Optional parent span ID
            tags: Optional span tags
            
        Returns:
            Span ID
        """
        span_id = str(uuid.uuid4())
        trace_id = trace_id or str(uuid.uuid4())
        
        span = Span(
            span_id=span_id,
            trace_id=trace_id,
            parent_span_id=parent_span_id or self._current_span_id,
            name=name,
            start_time=datetime.now(),
            tags=tags or {},
            metadata={}
        )
        
        self._active_spans[span_id] = span
        self._current_span_id = span_id
        
        # Record span start event
        self.monitor.record_event(Event(
            event_type=EventType.AGENT_START,
            timestamp=span.start_time,
            session_id=trace_id,
            metadata={
                "span_id": span_id,
                "parent_span_id": span.parent_span_id,
                "name": name,
                "tags": span.tags
            }
        ))
        
        return span_id
    
    def end_span(self, 
                span_id: str, 
                status: str = "success",
                error: Optional[str] = None) -> None:
        """End a span
        
        Args:
            span_id: ID of the span to end
            status: Final status of the span
            error: Optional error message
        """
        if span_id not in self._active_spans:
            raise KeyError(f"Span {span_id} not found")
            
        span = self._active_spans[span_id]
        span.end_time = datetime.now()
        span.status = status
        span.error = error
        
        # Record span end event
        event_type = (
            EventType.AGENT_ERROR if status == "error"
            else EventType.AGENT_COMPLETE
        )
        
        self.monitor.record_event(Event(
            event_type=event_type,
            timestamp=span.end_time,
            session_id=span.trace_id,
            duration_ms=self._calculate_duration_ms(span),
            status=status,
            error=error,
            metadata={
                "span_id": span_id,
                "parent_span_id": span.parent_span_id,
                "name": span.name,
                "tags": span.tags
            }
        ))
        
        # Update current span to parent
        if self._current_span_id == span_id:
            self._current_span_id = span.parent_span_id
            
        del self._active_spans[span_id]
    
    def add_metadata(self, span_id: str, metadata: Dict[str, Any]) -> None:
        """Add metadata to a span
        
        Args:
            span_id: ID of the span
            metadata: Metadata to add
        """
        if span_id not in self._active_spans:
            raise KeyError(f"Span {span_id} not found")
            
        span = self._active_spans[span_id]
        span.metadata.update(metadata)
    
    def get_active_spans(self) -> List[Span]:
        """Get all active spans
        
        Returns:
            List of active spans
        """
        return list(self._active_spans.values())
    
    def _calculate_duration_ms(self, span: Span) -> float:
        """Calculate span duration in milliseconds
        
        Args:
            span: Span to calculate duration for
            
        Returns:
            Duration in milliseconds
        """
        if not span.end_time:
            return 0.0
            
        duration = span.end_time - span.start_time
        return duration.total_seconds() * 1000

class TracedMixin:
    """Mixin class to add tracing capabilities to any class"""
    
    def __init__(self, tracer: Tracer):
        self.tracer = tracer
    
    def trace(self, name: str, tags: Optional[Dict[str, str]] = None) -> 'SpanContext':
        """Create a new traced context
        
        Args:
            name: Name of the span
            tags: Optional span tags
            
        Returns:
            Span context manager
        """
        return SpanContext(self.tracer, name, tags)

class SpanContext:
    """Context manager for trace spans"""
    
    def __init__(self, tracer: Tracer, name: str, tags: Optional[Dict[str, str]] = None):
        self.tracer = tracer
        self.name = name
        self.tags = tags
        self.span_id: Optional[str] = None
    
    def __enter__(self) -> str:
        self.span_id = self.tracer.start_span(self.name, tags=self.tags)
        return self.span_id
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.tracer.end_span(
                self.span_id,
                status="error",
                error=str(exc_val)
            )
        else:
            self.tracer.end_span(self.span_id) 