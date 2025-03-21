from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, model_validator
from datetime import datetime

class Message(BaseModel):
    """Represents a message in a conversation with an AI agent."""
    role: str = Field(..., description="The role of the message sender (e.g., 'system', 'user', 'assistant')")
    content: str = Field(..., description="The content of the message")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the message was created")

class Memory(BaseModel):
    """Represents an agent's memory of past interactions or knowledge."""
    id: str = Field(..., description="Unique identifier for the memory")
    content: str = Field(..., description="The content of the memory")
    source: str = Field(..., description="Where this memory came from")
    importance: int = Field(default=1, ge=1, le=10, description="How important this memory is (1-10)")
    created_at: datetime = Field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = Field(default=None)
    
    @model_validator(mode='after')
    def validate_importance(self) -> 'Memory':
        if self.importance < 1 or self.importance > 10:
            raise ValueError("Importance must be between 1 and 10")
        return self

class Tool(BaseModel):
    """Represents a tool that an agent can use."""
    name: str = Field(..., description="Name of the tool")
    description: str = Field(..., description="Description of what the tool does")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Parameters the tool accepts")
    required_parameters: List[str] = Field(default_factory=list, description="List of required parameter names")
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validates that all required parameters are present."""
        return all(param in params for param in self.required_parameters)

class AgentAction(BaseModel):
    """Represents an action taken by the agent."""
    action_type: str = Field(..., description="Type of action (e.g., 'tool_use', 'response')")
    content: Optional[str] = Field(None, description="Content of the action if applicable")
    tool_name: Optional[str] = Field(None, description="Name of the tool used if applicable")
    tool_parameters: Optional[Dict[str, Any]] = Field(None, description="Parameters passed to the tool")
    timestamp: datetime = Field(default_factory=datetime.now)

class AgentThought(BaseModel):
    """Represents the internal reasoning process of an agent."""
    content: str = Field(..., description="The thought content")
    timestamp: datetime = Field(default_factory=datetime.now)

class Agent(BaseModel):
    """Main Agent model that orchestrates behavior."""
    id: str = Field(..., description="Unique identifier for the agent")
    name: str = Field(..., description="The agent's name")
    description: str = Field(..., description="Description of the agent's purpose")
    available_tools: List[Tool] = Field(default_factory=list, description="Tools available to this agent")
    messages: List[Message] = Field(default_factory=list, description="Conversation history")
    memories: List[Memory] = Field(default_factory=list, description="Agent's memories")
    thoughts: List[AgentThought] = Field(default_factory=list, description="Agent's thought process")
    actions: List[AgentAction] = Field(default_factory=list, description="Actions taken by the agent")
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.messages.append(Message(role=role, content=content))
    
    def add_thought(self, content: str) -> None:
        """Add a thought to the agent's thought process."""
        self.thoughts.append(AgentThought(content=content))
        
    def add_memory(self, memory: Memory) -> None:
        """Add a memory to the agent's memory store."""
        self.memories.append(memory)
    
    def record_action(self, action: AgentAction) -> None:
        """Record an action taken by the agent."""
        self.actions.append(action)
