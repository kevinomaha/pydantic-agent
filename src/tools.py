"""
Tools that can be used by the PydanticAgent.
Each tool is defined as a function and wrapped with a Tool model.
"""

import json
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional
import os

from .models import Tool

def create_weather_tool() -> Tool:
    """Create a weather tool that can fetch weather information for a location."""
    return Tool(
        name="get_weather",
        description="Get current weather information for a location",
        parameters={
            "location": "The city and state or country (e.g., 'New York, NY' or 'London, UK')"
        },
        required_parameters=["location"]
    )

def create_search_tool() -> Tool:
    """Create a web search tool."""
    return Tool(
        name="web_search",
        description="Search the web for information",
        parameters={
            "query": "The search query",
            "num_results": "Number of results to return (default: 5)"
        },
        required_parameters=["query"]
    )

def create_calculator_tool() -> Tool:
    """Create a calculator tool for mathematical operations."""
    return Tool(
        name="calculator",
        description="Perform a mathematical calculation",
        parameters={
            "expression": "The mathematical expression to evaluate (e.g., '2 + 2')"
        },
        required_parameters=["expression"]
    )

def create_time_tool() -> Tool:
    """Create a tool that returns the current date and time."""
    return Tool(
        name="get_time",
        description="Get the current date and time",
        parameters={
            "timezone": "Optional timezone (default: UTC)"
        },
        required_parameters=[]
    )

# Example implementations of tool functions
def get_weather(location: str) -> Dict[str, Any]:
    """
    Get current weather for a location.
    
    In a real implementation, this would call a weather API.
    This is a mock implementation for demonstration purposes.
    """
    # Mock implementation
    weather_data = {
        "location": location,
        "temperature": 72,
        "condition": "Partly Cloudy",
        "humidity": 45,
        "wind_speed": 8,
        "timestamp": datetime.now().isoformat()
    }
    
    return weather_data

def web_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Search the web for information.
    
    In a real implementation, this would call a search API.
    This is a mock implementation for demonstration purposes.
    """
    # Mock implementation
    results = [
        {
            "title": f"Result {i+1} for '{query}'",
            "url": f"https://example.com/result{i+1}",
            "snippet": f"This is a snippet of information related to {query}..."
        }
        for i in range(min(num_results, 10))
    ]
    
    return results

def calculator(expression: str) -> Dict[str, Any]:
    """
    Evaluate a mathematical expression.
    
    Uses Python's eval function. In production, you would want to use
    a safer evaluation method.
    """
    try:
        # In a real implementation, you'd use a safer evaluation method
        # This is for demonstration only
        result = eval(expression, {"__builtins__": {}})
        return {
            "expression": expression,
            "result": result
        }
    except Exception as e:
        return {
            "expression": expression,
            "error": str(e)
        }

def get_time(timezone: Optional[str] = None) -> Dict[str, Any]:
    """
    Get the current date and time.
    
    In a real implementation, this would handle different timezones.
    This is a simplified implementation.
    """
    now = datetime.now()
    return {
        "datetime": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": timezone or "UTC"
    }
