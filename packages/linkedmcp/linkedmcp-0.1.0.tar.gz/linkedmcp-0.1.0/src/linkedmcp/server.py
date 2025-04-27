import asyncio
from mcp.server.lowlevel import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
import mcp.types as types
from pydantic import AnyUrl
from linkedmcp.helper import generate_pdf_from_text
# Initialize the server

server = Server("linkedmcp-server")

# =========================
# Tools
# =========================

TOOLS = [
    types.Tool(
        name="cover_letter_generator",
        description="Generate a custom cover letter for a specific job and return a PDF file.",
        inputSchema={
            "type": "object",
            "properties": {
                "job_title": {
                    "type": "string",
                    "description": "Job title you are applying for (e.g., 'DevOps Engineer').",
                },
                "company_name": {
                    "type": "string",
                    "description": "Name of the company (e.g., 'Google').",
                },
                "additional_details": {
                    "type": "string",
                    "description": "Any extra points to include (e.g., 'highlight leadership skills')",
                },
            },
            "required": ["job_title", "company_name"],
        },
    ),
    types.Tool(
        name="linkedin_profile_fixer",
        description="Suggest improvements to LinkedIn headline, about section, and experiences based on linkedin.txt",
        inputSchema={
            "type": "object",
            "properties": {
                "edited_profile_summary": {
                    "type": "string",
                    "description": "Updated LinkedIn profile summary or sections after AI improvements.",
                },
            },
            "required": ["edited_profile_summary"],
        }
    ),
    types.Tool(
        name="resume_editor",
        description="Apply AI-edited resume content to the stored resume file (resume.txt), and return a polished PDF.",
        inputSchema={
            "type": "object",
            "properties": {
                "edited_resume_text": {
                    "type": "string",
                    "description": "The updated full resume text after AI improvements.",
                },
            },
            "required": ["edited_resume_text"],
        }
    ),
]

# List the available tools
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return TOOLS

# --- Tool Handlers ---

@server.call_tool()
async def resume_editor_handler(input_data: dict) -> types.CallToolResult:
    edited_text = input_data["edited_resume_text"]

    # Save updated resume text to file
    with open("resume.txt", "w") as f:
        f.write(edited_text)

    # Generate PDF
    pdf_bytes = generate_pdf_from_text(edited_text)

    return types.ToolResult(
        file=pdf_bytes,
        mime_type="application/pdf"
    )

@server.call_tool()
async def cover_letter_generator_handler(input_data: dict) -> types.CallToolResult:
    job_title = input_data["job_title"]
    company_name = input_data["company_name"]
    additional_details = input_data.get("additional_details", "")

    # Create a simple cover letter text (you can make this much fancier later)
    cover_letter_text = f"""Dear {company_name} Hiring Team,

                            I am excited to apply for the {job_title} position at {company_name}. {additional_details}

                            Thank you for considering my application.

                            Sincerely,
                            [Your Name]
                        """

    # Generate PDF
    pdf_bytes = generate_pdf_from_text(cover_letter_text)

    return types.ToolResult(
        file=pdf_bytes,
        mime_type="application/pdf"
    )

@server.call_tool()
async def linkedin_profile_fixer_handler(input_data: dict) -> types.CallToolResult:
    edited_summary = input_data["edited_profile_summary"]

    # Save to file if you want
    with open("linkedin.txt", "w") as f:
        f.write(edited_summary)

    return types.ToolResult(
        message="LinkedIn profile updated successfully! ✅"
    )


# =========================
# Resources
# =========================

# Dummy in-memory "resources" (later you can hook this to real files, databases, etc)
RESOURCE_DATA = {
    "file:///linkedmcp/resume.txt": "Users LinkedIn Resume text...",
    "file:///linkedmcp/job_description.txt": "Job Description...",
    "file:///linkedmcp/profile_summary.txt": "User LinkedIn profile summary...",
    "file:///linkedmcp/cover_letter.txt": "Users cover letter",
}

@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri=uri,
            name=uri.split("/")[-1],
            mimeType="text/plain",
        )
        for uri in RESOURCE_DATA.keys()
    ]

@server.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    uri_str = str(uri)
    if uri_str in RESOURCE_DATA:
        return RESOURCE_DATA[uri_str]
    else:
        raise ValueError(f"Resource {uri_str} not found")

# =========================
# Main
# =========================

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="linkedmcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
