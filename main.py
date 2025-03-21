import os
import logging
from dotenv import load_dotenv

from src.agent import PydanticAgent
from src.tools import (
    create_weather_tool,
    create_search_tool,
    create_calculator_tool,
    create_time_tool
)

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        logger.error("OPENAI_API_KEY environment variable not set. Please set it in a .env file or export it.")
        return
    
    # Create the agent
    system_prompt = """You are a helpful AI assistant that can use tools to answer questions.
    When using tools, follow this format:
    
    Using tool: [tool_name]
    Parameters: [parameters as JSON]
    
    After using a tool, incorporate the results into your response.
    Be helpful, accurate, and concise.
    """
    
    agent = PydanticAgent(
        name="ToolUsingAssistant",
        description="An assistant that can use various tools to answer questions",
        system_prompt=system_prompt
    )
    
    # Add tools to the agent
    agent.add_tool(create_weather_tool())
    agent.add_tool(create_search_tool())
    agent.add_tool(create_calculator_tool())
    agent.add_tool(create_time_tool())
    
    # Add some memories
    agent.add_memory(
        content="Python is a high-level, interpreted programming language known for its readability and versatility.",
        source="agent_knowledge_base",
        importance=7
    )
    
    agent.add_memory(
        content="The user seems to prefer concise, direct answers.",
        source="user_preference_analysis",
        importance=6
    )
    
    # Interactive CLI
    print(f"🤖 {agent.agent_model.name} initialized!")
    print(f"Description: {agent.agent_model.description}")
    print(f"Available tools: {', '.join(tool.name for tool in agent.agent_model.available_tools)}")
    print("Type 'exit' to quit.")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("🤖 Goodbye!")
            break
        
        response = agent.process_user_input(user_input)
        print(f"\n🤖: {response}\n")
        
        # Debug option
        if user_input.lower() == "debug":
            print("\n--- AGENT DEBUG INFO ---")
            print(f"Messages: {len(agent.agent_model.messages)}")
            print(f"Thoughts: {len(agent.agent_model.thoughts)}")
            print(f"Latest thought: {agent.agent_model.thoughts[-1].content if agent.agent_model.thoughts else 'None'}")
            print(f"Actions: {len(agent.agent_model.actions)}")
            print(f"Memories: {len(agent.agent_model.memories)}")
            print("--- END DEBUG INFO ---\n")

if __name__ == "__main__":
    main()
