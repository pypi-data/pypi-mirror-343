import asyncio
import json
from pathlib import Path
from typing import Annotated, Any, Dict, List

import typer
from dotenv import load_dotenv
from rich.console import Console

from freeact import (
    Claude,
    CodeActAgent,
    CodeActModel,
    DeepSeekR1,
    DeepSeekV3,
    Gemini,
    QwenCoder,
    execution_environment,
)
from freeact.cli.utils import read_file, stream_conversation

app = typer.Typer()


async def amain(
    api_key: str | None,
    base_url: str | None,
    model_name: str,
    ipybox_tag: str,
    workspace_path: Path,
    workspace_key: str,
    skill_modules: List[str] | None,
    mcp_servers: Path | None,
    system_extension: Path | None,
    temperature: float,
    max_tokens: int,
    show_token_usage: bool,
    record_conversation: bool,
    record_path: Path,
):
    async with execution_environment(
        ipybox_tag=ipybox_tag,
        workspace_path=workspace_path,
        workspace_key=workspace_key,
    ) as env:
        async with env.code_provider() as provider:
            if mcp_servers:
                server_params = await read_file(mcp_servers)
                server_params_dict = json.loads(server_params)
                tool_names = await provider.register_mcp_servers(server_params_dict["mcpServers"])
            else:
                tool_names = {}

            if skill_modules or tool_names:
                skill_sources = await provider.get_sources(module_names=skill_modules, mcp_tool_names=tool_names)
            else:
                skill_sources = None

        if system_extension:
            system_extension_str = await read_file(system_extension)
        else:
            system_extension_str = None

        run_kwargs: Dict[str, Any] = {
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        model: CodeActModel

        if "claude" in model_name.lower():
            model = Claude(
                model_name=model_name,  # type: ignore
                system_extension=system_extension_str,
                prompt_caching=True,
                api_key=api_key,
                base_url=base_url,
            )
            run_kwargs |= {"skill_sources": skill_sources}
        elif "gemini" in model_name.lower():
            model = Gemini(
                model_name=model_name,  # type: ignore
                skill_sources=skill_sources,
                api_key=api_key,
                base_url=base_url,
            )
        elif "qwen" in model_name.lower():
            model = QwenCoder(
                model_name=model_name,
                skill_sources=skill_sources,
                api_key=api_key,
                base_url=base_url,
            )
        elif "deepseek-v3" in model_name.lower():
            model = DeepSeekV3(
                model_name=model_name,
                skill_sources=skill_sources,
                api_key=api_key,
                base_url=base_url,
            )
        elif "deepseek-r1" in model_name.lower():
            model = DeepSeekR1(
                model_name=model_name,
                skill_sources=skill_sources,
                api_key=api_key,
                base_url=base_url,
            )
        else:
            typer.echo(f"Unsupported model: {model_name}", err=True)
            raise typer.Exit(code=1)

        if record_conversation:
            console = Console(record=True, width=120, force_terminal=True)
        else:
            console = Console()

        async with env.code_executor() as executor:
            agent = CodeActAgent(model=model, executor=executor)
            await stream_conversation(agent, console, **run_kwargs, show_token_usage=show_token_usage)

        if record_conversation:
            console.save_svg(str(record_path), title="")


@app.command()
def main(
    model_name: Annotated[str, typer.Option(help="Name of the model")] = "anthropic/claude-3-5-sonnet-20241022",
    api_key: Annotated[str | None, typer.Option(help="API key of the model")] = None,
    base_url: Annotated[str | None, typer.Option(help="Base URL of the model")] = None,
    ipybox_tag: Annotated[str, typer.Option(help="Tag of the ipybox Docker image")] = "ghcr.io/gradion-ai/ipybox:basic",
    workspace_path: Annotated[Path, typer.Option(help="Path to the workspace directory")] = Path("workspace"),
    workspace_key: Annotated[str, typer.Option(help="Key for private workspace directories")] = "default",
    skill_modules: Annotated[List[str] | None, typer.Option(help="Skill modules to load")] = None,
    mcp_servers: Annotated[Path | None, typer.Option(help="Path to a MCP servers file")] = None,
    system_extension: Annotated[Path | None, typer.Option(help="Path to a system extension file")] = None,
    temperature: Annotated[float, typer.Option(help="Temperature for generating model responses")] = 0.0,
    max_tokens: Annotated[int, typer.Option(help="Maximum number of tokens for each model response")] = 8192,
    show_token_usage: Annotated[bool, typer.Option(help="Include token usage data in responses")] = False,
    record_conversation: Annotated[bool, typer.Option(help="Record conversation as SVG file")] = False,
    record_path: Annotated[Path, typer.Option(help="Path to the SVG file")] = Path("conversation.svg"),
):
    asyncio.run(amain(**locals()))


if __name__ == "__main__":
    load_dotenv()
    app()
