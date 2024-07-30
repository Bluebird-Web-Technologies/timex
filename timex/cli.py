import click
from manager import ProjectManager


@click.group()
def cli():
    """A simple CLI for project management."""


@click.command()
@click.argument("project_name")
def new(project_name) -> None:
    """Create a new project."""

    pm.new_project(project_name)
    click.echo(f"Creates a new project {project_name}!")


@click.command(name="list")
def list_projects():
    """List all projects"""
    projects = pm.all_projects()

    for project in projects:
        click.echo(f"  - {project[0]}")


@click.command()
@click.argument("project_name")
@click.option("--description", default=None, help="Optional description of activity")
@click.argument("tags", nargs=-1)
def start(project_name, description, tags):
    processed_tags = [tag.lstrip("+") for tag in tags]

    pm.start_activity(project_name, description, processed_tags)


cli.add_command(new)
cli.add_command(list)
cli.add_command(start)

pm: ProjectManager = ProjectManager()

if __name__ == "__main__":
    cli()
