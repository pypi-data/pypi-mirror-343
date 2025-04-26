import os
import shutil
import click
import lamini

base_dir = os.path.dirname(lamini.__file__)


@click.group()
def cli():
    """CLI tool for scaffolding projects."""
    pass


@cli.command()
@click.argument("project_type")
@click.argument("project_name")
def create(project_type, project_name):
    """
    Create a new project based on the specified template.
    PROJECT_TYPE: Type of project (e.g., 'Q&A')
    PROJECT_NAME: Name of the new project
    """
    template_dir = os.path.join(base_dir, "project_templates", project_type)
    if not os.path.exists(template_dir):
        click.echo(f"Template for project type '{project_type}' does not exist.")
        return

    target_dir = os.path.join(os.getcwd(), project_name)
    if os.path.exists(target_dir):
        click.echo(f"Project '{project_name}' already exists.")
        return

    shutil.copytree(template_dir, target_dir)
    click.echo(
        f"Project '{project_name}' created successfully using the '{project_type}' template."
    )


if __name__ == "__main__":
    cli()
