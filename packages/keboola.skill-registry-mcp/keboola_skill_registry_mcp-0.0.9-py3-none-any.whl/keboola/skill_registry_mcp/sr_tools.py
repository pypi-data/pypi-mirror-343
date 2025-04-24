from typing import Callable, List, Any, Optional

from mcp.server.fastmcp import Context
from mcp.server.session import ServerSessionT
from mcp.shared.context import LifespanContextT
from mcp.types import Tool as MCPTool
from pydantic import BaseModel

from .client import SkillRegistryClient, Skill


class JsonSchemaProperty(BaseModel):
    """A property in a JSON Schema.

    Args:
        type: The data type of the property (e.g. "string", "number", "object")
        description: Human readable description of what the property represents
        required: Whether this property is required in the schema
    """

    type: str
    description: Optional[str] = None
    required: bool = False


class ToolInputSchema(BaseModel):
    """Input schema for a tool.

    Args:
        type: Always "object" for this schema
        required: List of required property names
        properties: Dictionary mapping property names to their JsonSchemaProperty definitions
    """

    type: str = "object"
    required: list[str]
    properties: dict[str, JsonSchemaProperty]


def _skill_to_tool(skill: Skill) -> MCPTool:
    required_params = list()
    properties = {}
    for parameter in skill.properties:
        if parameter.required:
            required_params.append(parameter.name)
        property_schema = JsonSchemaProperty(
            type=parameter.type, description=parameter.description, required=parameter.required
        )
        properties[parameter.name] = property_schema

    input_schema = ToolInputSchema(required=required_params, properties=properties)

    tool = MCPTool(name=skill.name, description=skill.description, inputSchema=dict(input_schema))

    return tool


def create_skill_function(skill_id: str) -> Callable:
    async def execute(ctx: Context, **kwargs):
        client: SkillRegistryClient = ctx.request_context.lifespan_context.sr_client
        # Call API to execute the skill
        return client.execute_skill(skill_id, kwargs)

    return execute


def _normalize_tool_name(name: str) -> str:
    """Normalize the tool name to a consistent format.

    Converts name to lowercase, reduces multiple spaces to single space,
    then replaces spaces with underscores.
    """
    normalized = " ".join(name.lower().split())  # Reduce multiple spaces to single space
    return normalized.replace(" ", "_")


class SRToolManager:
    @classmethod
    def from_skill_registry(cls, client: SkillRegistryClient) -> "SRToolManager":
        tool_definitions = list()
        skill_mapping = dict()

        for skill in client.list_skills():
            skill.name = _normalize_tool_name(skill.name)
            tool_definitions.append(_skill_to_tool(skill))
            skill_mapping[skill.name] = create_skill_function(skill.id)

        return cls(tool_definitions, skill_mapping)

    def __init__(self, tool_definitions: List[MCPTool], tool_mapping: dict[str, Callable]):
        self._tool_definitions = tool_definitions
        self._tool_mapping = tool_mapping

    def list_tool_names(self) -> List[str]:
        """List all tool names."""
        return [tool.name for tool in self._tool_definitions]

    def list_tools(self) -> List[MCPTool]:
        return self._tool_definitions

    def call_tool(
        self,
        name: str,
        arguments: dict[str, Any],
        context: Context[ServerSessionT, LifespanContextT] | None = None,
    ) -> Any:
        return self._tool_mapping[name](ctx=context, **arguments)
