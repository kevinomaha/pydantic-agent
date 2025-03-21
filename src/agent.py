import os
import uuid
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from langchain.prompts import ChatPromptTemplate
from langchain.llms import OpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from .models import Agent, Message, Memory, Tool, AgentAction, AgentThought

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PydanticAgent:
    """Implementation of an AI agent using Pydantic models for structure and validation."""
    
    def __init__(self, name: str, description: str, system_prompt: str, openai_api_key: Optional[str] = None):
        """Initialize a new PydanticAgent.
        
        Args:
            name: Name of the agent
            description: Description of the agent's purpose
            system_prompt: The system prompt that guides the agent's behavior
            openai_api_key: OpenAI API key, defaults to environment variable OPENAI_API_KEY
        """
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key must be provided or set as OPENAI_API_KEY environment variable")
        
        self.llm = OpenAI(api_key=self.api_key)
        self.agent_model = Agent(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            available_tools=[],
            messages=[Message(role="system", content=system_prompt)],
            memories=[],
            thoughts=[],
            actions=[]
        )
        
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the agent's available tools."""
        self.agent_model.available_tools.append(tool)
        logger.info(f"Added tool: {tool.name}")
        
    def add_memory(self, content: str, source: str, importance: int = 5) -> None:
        """Add a new memory to the agent."""
        memory = Memory(
            id=str(uuid.uuid4()),
            content=content,
            source=source,
            importance=importance
        )
        self.agent_model.add_memory(memory)
        logger.info(f"Added memory: {memory.id}")
        
    def _get_prompt_messages(self) -> List[Dict[str, str]]:
        """Convert agent's messages to format expected by LangChain."""
        prompt_messages = []
        for msg in self.agent_model.messages:
            prompt_messages.append({"role": msg.role, "content": msg.content})
        return prompt_messages
        
    def _format_tools_for_prompt(self) -> str:
        """Format the available tools as a string for the prompt."""
        if not self.agent_model.available_tools:
            return "No tools available."
            
        tool_descriptions = []
        for tool in self.agent_model.available_tools:
            params_desc = ", ".join([f"{param} (required)" if param in tool.required_parameters 
                                   else param for param in tool.parameters])
            tool_descriptions.append(f"Tool: {tool.name}\nDescription: {tool.description}\nParameters: {params_desc}\n")
            
        return "\n".join(tool_descriptions)
        
    def _think(self, user_input: str) -> str:
        """Generate agent thoughts about how to respond to user input."""
        thinking_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an AI assistant thinking step by step about how to respond to a user. " 
                                "Think through what tools might be useful and how to structure your response."),
            HumanMessage(content=f"User input: {user_input}\n\nAvailable tools:\n{self._format_tools_for_prompt()}\n\n"
                                f"Think step by step about how to respond to this user request.")
        ])
        
        thought_chain = thinking_prompt | self.llm | StrOutputParser()
        thought = thought_chain.invoke({})
        
        self.agent_model.add_thought(thought)
        return thought
        
    def process_user_input(self, user_input: str) -> str:
        """Process user input and generate a response."""
        # Add user message to conversation history
        self.agent_model.add_message(role="user", content=user_input)
        
        # Generate thoughts about how to respond
        self._think(user_input)
        
        # Create main prompt
        main_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self.agent_model.messages[0].content),  # System prompt
            HumanMessage(content=f"Available tools:\n{self._format_tools_for_prompt()}\n\n"
                                f"User input: {user_input}")
        ])
        
        # Generate response
        response_chain = main_prompt | self.llm | StrOutputParser()
        response = response_chain.invoke({})
        
        # Record response as an action
        self.agent_model.record_action(
            AgentAction(
                action_type="response",
                content=response
            )
        )
        
        # Add assistant message to conversation history
        self.agent_model.add_message(role="assistant", content=response)
        
        return response
