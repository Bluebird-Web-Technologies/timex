#!/home/ben/.cache/pypoetry/virtualenvs/timex-gL4yf6b8-py3.11/bin/python

from datetime import datetime

import click
from exceptions import ActivityAlreadyActiveError
from exceptions import ModelAlreadyExistsError
from exceptions import ModelNotFoundError
from manager import ProjectManager
from utils import str_format_duration


def info(message):
    click.echo(message)


def warn(message):
    click.echo(click.style(message, fg="yellow"))


@click.group()
def cli():
    """A simple CLI for project management."""


@click.command()
@click.argument("project_name")
def new(project_name) -> None:
    """Create a new project."""

    try:
        pm.new_project(project_name)
        click.echo(f"Creates a new project {project_name}!")
    except ModelAlreadyExistsError as e:
        warn(e.message)


@click.command(name="list")
def list_projects():
    """List all projects"""
    projects = pm.all_projects()

    for project in projects:
        click.echo(f"  - {project[0]}")


@click.command()
def stop():
    try:
        duration = pm.stop_activity()
    except ModelNotFoundError:
        warn("There is not an activity to stop")
        return

    duration_str = str_format_duration(duration)

    click.echo("Activity stopped. Total time: " + duration_str)


@click.command()
@click.argument("project_name")
@click.option("--description", default=None, help="Optional description of activity")
@click.argument("tags", nargs=-1)
def start(project_name, description, tags):
    processed_tags = [tag.lstrip("+") for tag in tags]

    try:
        pm.start_activity(project_name, description, processed_tags)
        click.echo("Activity start! Go get it! 🚀")
    except ActivityAlreadyActiveError:
        message: str = (
            "There is already an active activity. "
            "Stop that active before starting another"
        )
        warn(message)


@click.command()
def status():
    current_activity = pm.current_activity()

    # Early Exit
    if current_activity is None:
        info("You aren't current working on a project")
        return

    project = current_activity.project

    duration = datetime.now(tz=datetime.timezone.utc) - current_activity.starts_at
    duration_str = str_format_duration(duration)

    info(f"You have been working on {project.name} for {duration_str}")


cli.add_command(new)
cli.add_command(list_projects)
cli.add_command(start)
cli.add_command(stop)
cli.add_command(status)

pm: ProjectManager = ProjectManager()

if __name__ == "__main__":
    cli()
