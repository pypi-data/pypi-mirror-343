from mcp.server import Server
import mcp.types as types
from .server import mcp

PROMPTS = {
    "linkedin-story": types.Prompt(
        name="linkedin-story",
        description="Generate a personal story post for LinkedIn",
        arguments=[
            types.PromptArgument(name="topic", description="What is the post about?", required=True),
            types.PromptArgument(name="lesson", description="What did you learn?", required=False),
        ]
    ),
    "linkedin-launch": types.Prompt(
        name="linkedin-launch",
        description="Generate a LinkedIn launch announcement",
        arguments=[
            types.PromptArgument(name="project", description="Name of your project", required=True),
            types.PromptArgument(name="description", description="What does it do?", required=True),
        ]
    ),
}

@mcp.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return list(PROMPTS.values())

@mcp.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None = None) -> types.GetPromptResult:
    if name not in PROMPTS:
        raise ValueError(f"Prompt not found: {name}")

    if name == "linkedin-story":
        topic = arguments.get("topic", "")
        lesson = arguments.get("lesson", "")
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Write a personal LinkedIn post about this topic: {topic}."
                             f"\nInclude a story, some vulnerability, and a professional takeaway."
                             f"\nOptional lesson: {lesson}"
                    )
                )
            ]
        )

    if name == "linkedin-launch":
        project = arguments.get("project", "")
        desc = arguments.get("description", "")
        return types.GetPromptResult(
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Write a professional LinkedIn post announcing the launch of {project}. "
                             f"Explain what it does: {desc}. Include enthusiasm and a call to action."
                    )
                )
            ]
        )

    raise ValueError("Prompt not implemented.")
