import click

import os
from pathlib import Path


from cookiecutter.main import cookiecutter


BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = os.path.join(BASE_DIR / "templates")


@click.group()
def cli():
	pass


@cli.command("create_project", help="Create aiogram project")
@click.argument("name")
def create_project(name: str):
	click.echo(f"Creating project with name {name}")

	cookiecutter(
		os.path.join(TEMPLATES_DIR, "project_template"),
		extra_context={"project_name": name},
		output_dir=".",
		no_input=True
	)

	click.echo(f"Project {name} created successfully!")

	cookiecutter(
		os.path.join(TEMPLATES_DIR, "main_app_template"),
		extra_context={"app_name": "main"},
		output_dir=f"./{name}/apps/",
		no_input=True
	)

	click.echo(f"App main for project {name} created successfully!")


@cli.command("create_app", help="Create an app in your project")
@click.argument("name")
def create_project(name: str):
	if "manage.py" not in os.listdir(".") and (not open("./manage.py").read().startswith("#AIOGRAM_MANAGER")):
		return click.echo("Seems like you are not in aiogram_manager project!")

	click.echo(f"Creating app with name {name}")

	cookiecutter(
		os.path.join(TEMPLATES_DIR, "app_template"),
		extra_context={"app_name": name},
		output_dir=f"./apps/",
		no_input=True
	)

	click.echo(f"App {name} created successfully!")



