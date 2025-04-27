"""Example agent implementation using Google Gemini API with configuration.

This example demonstrates how to create an agent that uses the Google Gemini API
with the MCPS configuration system.
"""

import os
import sys
import logging
from typing import Dict, Any, Optional

from mcps.config.base import BaseConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GeminiAgentConfig(BaseConfig):
    """Configuration for Gemini agent."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize Gemini agent configuration.
        
        Args:
            config_path: Optional path to a configuration file
        """
        super().__init__(config_path)
        
        self._config.setdefault("api_key", os.environ.get("GEMINI_API_KEY", ""))
        self._config.setdefault("model", "gemini-2.0-flash")
        self._config.setdefault("max_tokens", 1024)
        self._config.setdefault("temperature", 0.7)
        
        safe_config = self._config.copy()
        if "api_key" in safe_config:
            safe_config["api_key"] = "***" if safe_config["api_key"] else "not set"
        logger.info(f"Gemini agent configuration: {safe_config}")

def run_agent(context: Dict[str, Any]) -> Dict[str, Any]:
    """Run agent with Google Gemini API.
    
    Args:
        context: Execution context with a 'query' field and optional 'config_path'
        
    Returns:
        Agent result with 'result' and optional 'error' fields
    """
    query = context.get("query", "")
    config_path = context.get("config_path")
    
    config = GeminiAgentConfig(config_path)
    api_key = config.get("api_key")
    model = config.get("model")
    
    if not api_key:
        return {
            "result": "Error: GEMINI_API_KEY not set in configuration or environment",
            "error": "ConfigurationError"
        }
    
    try:
        from google import genai
    except ImportError:
        return {
            "result": "Error: google-genai package not installed. Install with: pip install google-genai",
            "error": "ImportError"
        }
    
    try:
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model=model,
            contents=query
        )
        
        return {
            "result": response.text,
            "model": model
        }
    except Exception as e:
        return {
            "result": f"Error calling Gemini API: {str(e)}",
            "error": type(e).__name__
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_query = sys.argv[1]
    else:
        test_query = "Explain how AI works in a few words"
    
    import tempfile
    import json
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as f:
        config_path = f.name
        json.dump({
            "api_key": os.environ.get("GEMINI_API_KEY", ""),
            "model": "gemini-2.0-flash"
        }, f)
    
    test_result = run_agent({
        "query": test_query,
        "config_path": config_path
    })
    
    print(f"Query: {test_query}")
    print(f"Response: {test_result['result']}")
    
    os.unlink(config_path)
else:
    try:
        result = run_agent(context)
    except NameError:
        pass
