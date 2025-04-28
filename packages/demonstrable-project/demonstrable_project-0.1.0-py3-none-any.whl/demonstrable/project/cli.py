import importlib.resources
import pathlib
import shutil
import subprocess
import sys
import click
import exit_codes
from . import __version__
import logging
import demonstrable.project.package_data

CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    token_normalize_func=lambda x: x.replace("-", "_"),
)

logger = logging.getLogger(__name__)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--verbosity",
    "-v",
    default=None,
    help="The logging level to use.",
    type=click.Choice(
        [name for lvl, name in sorted(logging._levelToName.items()) if lvl > 0],
        case_sensitive=False,
    ),
)
@click.version_option(__version__)
def cli(verbosity):
    logging_level = verbosity and getattr(logging, verbosity.upper(), None)

    kwargs = {}
    if logging_level is None:
        kwargs["format"] = "%(message)s"  # By default, simplify message output
    else:
        kwargs["level"] = logging_level

    logging.basicConfig(**kwargs)


@cli.command()
@click.argument("project_path", type=click.Path(exists=False, path_type=pathlib.Path))
def create_project(project_path):
    """Create a new project."""
    logger.info(f"Creating a new project at {project_path}")

    with importlib.resources.path(demonstrable.project.package_data, "new_project") as src:
        shutil.copytree(src, project_path)

    logger.info("Syncing the project depedendencies")
    _run_process("uv sync", project_path)

    logger.info("Initialize the deca project")
    _run_process("uv run deca init", project_path)

    logger.info("Creating a deca recipe")
    _run_process("uv run deca create-recipe", project_path)

def _run_process(command, cwd):
    try:
        subprocess.run(command, cwd=cwd, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run '{command}' in {cwd}: {e}")
        logger.error(f"Process output: {e.output}")
        sys.exit(exit_codes.ExitCode.DATA_ERR)


def main():
    """Main entry point for the CLI."""
    cli(prog_name="demonstrable-project")


if __name__ == "__main__":
    main()