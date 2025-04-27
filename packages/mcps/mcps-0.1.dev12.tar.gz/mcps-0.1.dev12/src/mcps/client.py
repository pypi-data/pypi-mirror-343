from typing import List, Dict, Any, Optional
from .core.transports.base import BaseTransport, AuthToken
from .services.discovery.base import ServiceDescriptor, ServiceDiscoverer
from .agents.discovery.base import AgentDiscoverer, AgentMatch
from .agents.runtime.base import AgentRuntime, RuntimeEnvironment, ExecutionSession
from datetime import datetime

class MCPSClient:
    """Main client for MCPS service interactions"""
    
    def __init__(self, api_key: str, transport: Optional[BaseTransport] = None):
        self.api_key = api_key
        self.transport = transport
        self._service_discoverer: Optional[ServiceDiscoverer] = None
    
    def query(self, query: str, topk: int = 1) -> List[ServiceDescriptor]:
        """Query services using natural language
        
        Args:
            query: Natural language query
            topk: Number of top results to return
            
        Returns:
            List of matching service descriptors
        """
        if not self._service_discoverer:
            raise RuntimeError("Service discoverer not initialized")
        return self._service_discoverer.find_by_nlp(query, topk)
    
    def call_service(self, service_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific service
        
        Args:
            service_id: Service identifier
            params: Service parameters
            
        Returns:
            Service response
        """
        if not self.transport:
            raise RuntimeError("Transport not initialized")
            
        service = self._service_discoverer.get_service(service_id)
        response = self.transport.send_request({
            "service_id": service_id,
            "params": params
        })
        return response.data
    
    def call_with_fallback(self, primary_service: str, 
                          fallback_services: List[str],
                          **params) -> Dict[str, Any]:
        """Call service with fallback options
        
        Args:
            primary_service: Primary service ID
            fallback_services: List of fallback service IDs
            **params: Service parameters
            
        Returns:
            Service response from first successful call
        """
        services = [primary_service] + fallback_services
        last_error = None
        
        for service_id in services:
            try:
                return self.call_service(service_id, params)
            except Exception as e:
                last_error = e
                continue
                
        raise RuntimeError(f"All services failed. Last error: {last_error}")

class AgentsClient:
    """Client for agent interactions"""
    
    def __init__(self, api_key: str, runtime: AgentRuntime, discoverer: Optional[AgentDiscoverer] = None):
        self.api_key = api_key
        self.runtime = runtime
        self._agent_discoverer = discoverer
    
    def call_from_query(self, query: str, topl: int = 1) -> List[Dict[str, Any]]:
        """Find and call agents based on natural language query
        
        Args:
            query: Natural language query
            topl: Number of top results to return
            
        Returns:
            List of agent responses
        """
        if not self._agent_discoverer:
            raise RuntimeError("Agent discoverer not initialized")
            
        # Find matching agents
        matches: List[AgentMatch] = self._agent_discoverer.find_agents_by_query(query)
        
        # Sort by relevance and take top-l
        matches = sorted(matches, key=lambda x: x.score, reverse=True)[:topl]
        
        # Call each matching agent
        results = []
        for match in matches:
            try:
                result = self.call_agent(
                    agent_id=match.agent_id,
                    tools=match.metadata.get("tools", []),
                    query=query
                )
                results.append({
                    "agent_id": match.agent_id,
                    "score": match.score,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "agent_id": match.agent_id,
                    "score": match.score,
                    "error": str(e)
                })
                
        return results
    
    def call_agent(self, agent_id: str, tools: List[str], query: str) -> Dict[str, Any]:
        """Call a specific agent
        
        Args:
            agent_id: Agent identifier
            tools: List of tool IDs to use
            query: Agent query/instruction
            
        Returns:
            Agent response
        """
        session = ExecutionSession(
            session_id=f"session_{agent_id}_{datetime.now().timestamp()}",
            agent_id=agent_id,
            start_time=datetime.now(),
            context={"query": query},
            tools=tools
        )
        
        result = self.runtime.execute(session)
        return result.result 