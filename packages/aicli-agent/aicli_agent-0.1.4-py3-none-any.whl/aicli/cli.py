import time

import click
import rich
from GeneralAgent import Agent

from aicli.conf import settings
from aicli.agentlib import get_general_agent, setup_agent
from aicli.tools import install_package, run_command, web_search, translate, read_link

@click.command()
@click.argument("query", required=False)
@click.option("-m", "--model", default="grok-2-1212")
@click.option("-l", "--token-limit", default=64000)
@click.option("-a", "--archive", is_flag=True)
@click.option("-ao", "--archive-output", is_flag=True)
@click.option(
    "-nc",
    "--no-context",
    is_flag=True,
    help="Single question mode without multi-turn context",
)
@click.option(
    "-ad",
    "--advanced",
    is_flag=True,
    help="Run advanced mode",
)
@click.option(
    "-sp",
    "--show-path",
    is_flag=True,
    help="Print all the folders for the current workspace",
)
def cli(query, model, token_limit, archive, archive_output, no_context, show_path, advanced):
    """CLI command to handle user query and interact with the agent."""
    if show_path:
        if settings.output_callback_path.exists():
            click.echo(f"Chat history path: {settings.output_callback_path}")
        if settings.workspace_path.exists():
            click.echo(f"Workspace path: {settings.workspace_path}")
        archive_path = settings.workspace_path.parent / "archive/"
        if archive_path.exists():
            for file in archive_path.iterdir():
                if settings.workspace_path.name in file.as_posix():
                    click.echo(f"Archived path: {file}")
        return

    if archive:
        try:
            name = settings.workspace_path.name
            readable_time = int(time.time())
            target_path = (
                settings.workspace_path.parent / f"archive/{name}_{readable_time}"
            )
            target_path.mkdir(exist_ok=True, parents=True)
            settings.workspace_path.rename(target_path)
            click.echo(f"move {settings.workspace_path} to {target_path}")
        except Exception as err:
            click.echo(f"error occurred: {err}")


    if archive_output:
        try:
            name = settings.output_callback_path.stem
            readable_time = int(time.time())
            target_path = (
                settings.output_callback_path.parent
                / f"archive/{name}_{readable_time}.md"
            )
            target_path.parent.mkdir(exist_ok=True, parents=True)
            settings.output_callback_path.rename(target_path)
            click.echo(f"move {settings.output_callback_path} to {target_path}")
        except Exception as err:
            click.echo(f"error occurred: {err}")

    if archive or archive_output:
        return

    if not query:
        print(">>> :")
        query = input()

    functions = [run_command, install_package, web_search, translate, read_link]
    agent: Agent = setup_agent(
        token_limit=token_limit, model=model, no_context=no_context, functions=functions
    )
    plan_agent: Agent = get_general_agent(model=model, token_limit=token_limit, role="你是一个任务规划专家，会把一个复杂的任务拆分成若干个小的步骤。")

    if advanced:
        tasks = plan_agent.run(
            f'Based on user query: <QUERY>{query}</QUERY>, generate a list of plan so you can use your tool or write python code to solve user problem',
            "return a list[str] of 1-10 steps that can be execute by write python code to finish user requirement.",
            display=True,
        )
        rich.print(tasks)
        for task in tasks:
            _ = agent.run(task, {"succeed": bool, "result": str})
        return

    result = agent.user_input(query)

    print("\n" * 3)
    if len(str(result).split()) < 4000:
        rich.print(result)
    else:
        rich.print(result[:4000])


if __name__ == "__main__":
    cli()
