"""The Strands Agent Loop Harness."""
import inspect
import json
from typing import List, Callable, Dict, Any, Optional
from .models import BedrockModel
from .memory import InMemoryMemory

class Agent:
    """Production Agent Harness connecting Foundation Models to Native Python Tools."""

    def __init__(
        self,
        model: BedrockModel,
        tools: Optional[List[Callable]] = None,
        system_prompt: str = "You are an autonomous AI agent.",
        memory: Optional[Any] = None,
        max_iterations: int = 5,
        name: str = "Agent"
    ):
        self.model = model
        self.system_prompt = system_prompt
        self.memory = memory or InMemoryMemory()
        self.max_iterations = max_iterations
        self.name = name
        self.raw_tools = tools or []
        self.tool_map: Dict[str, Callable] = {fn.__name__: fn for fn in self.raw_tools}
        self.tool_schemas = [self._generate_tool_schema(fn) for fn in self.raw_tools]

    def _generate_tool_schema(self, fn: Callable) -> Dict[str, Any]:
        """Extracts JSON schema from function docstring and type hints."""
        sig = inspect.signature(fn)
        doc = inspect.getdoc(fn) or "No description provided."
        properties: Dict[str, Any] = {}
        required: List[str] = []

        for param_name, param in sig.parameters.items():
            param_type = "string"
            if param.annotation == int:
                param_type = "integer"
            elif param.annotation == float:
                param_type = "number"
            elif param.annotation == bool:
                param_type = "boolean"
            elif param.annotation == dict or param.annotation == Dict[str, Any]:
                param_type = "object"

            properties[param_name] = {
                "type": param_type,
                "description": f"Parameter: {param_name}"
            }
            if param.default == inspect.Parameter.empty:
                required.append(param_name)

        return {
            "name": fn.__name__,
            "description": doc.split("\n\n")[0],
            "input_schema": {
                "type": "object",
                "properties": properties,
                "required": required,
            }
        }

    def run(self, prompt: str) -> str:
        """Executes the autonomous loop: reasoning -> tool selection -> tool execution -> reflection."""
        self.memory.add_message(role="user", content=prompt)
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            messages = self.memory.get_messages()

            # 1. Invoke Model
            response = self.model.invoke(
                system_prompt=self.system_prompt,
                messages=messages,
                tools=self.tool_schemas if self.tool_schemas else None
            )

            text_output = response.get("text", "")
            tool_calls = response.get("tool_calls", [])

            # Record model assistant message
            self.memory.add_message(role="assistant", content=text_output, tool_calls=tool_calls)

            # 2. If no tools were invoked, agent has completed its goal
            if not tool_calls:
                return text_output

            # 3. Execute Tool Calls
            for call in tool_calls:
                tool_name = call.get("name")
                args = call.get("arguments", {})
                target_fn = self.tool_map.get(tool_name)

                if not target_fn:
                    tool_result_str = f"Error: Tool '{tool_name}' not found."
                else:
                    try:
                        tool_result = target_fn(**args)
                        tool_result_str = json.dumps(tool_result, indent=2) if isinstance(tool_result, (dict, list)) else str(tool_result)
                    except Exception as e:
                        tool_result_str = f"Tool execution failed with exception: {str(e)}"

                # Feed tool result back to memory for reflection
                self.memory.add_message(
                    role="tool",
                    content=f"Tool '{tool_name}' output:\n{tool_result_str}"
                )

        return f"Agent reached maximum execution iterations ({self.max_iterations}). Final state:\n{self.memory.get_messages()[-1]['content']}"

