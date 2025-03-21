# Pydantic AI Agent

This project implements an AI agent using Pydantic data models for type validation and structure, integrated with LangChain and OpenAI for language processing capabilities.

## Features

- Structured agent architecture using Pydantic models
- Tool usage and integration framework
- Memory system for knowledge retention
- Thought process modeling for better reasoning
- Simple CLI interface for interaction

## Project Structure

```
pydantic-agent/
├── .env.example        # Example environment variables
├── main.py             # Main application entry point
├── requirements.txt    # Project dependencies
├── README.md           # This documentation
├── src/                # Source code
│   ├── __init__.py     # Package initialization
│   ├── agent.py        # Agent implementation
│   ├── models.py       # Pydantic data models
│   └── tools.py        # Tool definitions and implementations
└── tests/              # Test directory
```

## Setup

1. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file:
   ```
   cp .env.example .env
   ```

4. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

Run the interactive CLI:

```
python main.py
```

Example commands:
- Ask about the weather: "What's the weather in New York?"
- Perform calculations: "Calculate 15 * 24 + 7"
- Get the current time: "What time is it right now?"
- Exit the program: "exit"
- Show debug information: "debug"

## Extending the Agent

### Adding New Tools

1. Define a new tool creation function in `src/tools.py`:
   ```python
   def create_my_new_tool() -> Tool:
       return Tool(
           name="my_tool_name",
           description="Description of what the tool does",
           parameters={
               "param1": "Description of param1",
               "param2": "Description of param2"
           },
           required_parameters=["param1"]
       )
   ```

2. Implement the tool functionality.

3. Add the tool to the agent in `main.py`:
   ```python
   agent.add_tool(create_my_new_tool())
   ```

### Adding New Agent Capabilities

Modify the `PydanticAgent` class in `src/agent.py` to add new functionality.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
