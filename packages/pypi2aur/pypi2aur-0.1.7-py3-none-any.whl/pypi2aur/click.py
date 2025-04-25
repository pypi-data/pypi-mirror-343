import click
from . import createPKGBUILD, readPyPiDeps, updatePKGBUILD

# This is the version of the application.
APP_VERSION = "0.1.7"
APP_NAME = "pypi2aur"


def showNameAndVersion() -> None:
    """
    Show the name and version of the application.

    Returns:
        None
    """
    click.echo(f"{APP_NAME} version {APP_VERSION}\n")


@click.group()
# @click.version_option(APP_VERSION, "-v", "--version", message="%(version)s")
def cli() -> None:
    """pypi2aur - PyPi to AUR PKGBUILD generator and helper."""
    # Show program name and version on every invocation
    pass


@cli.command()
@click.argument("pkg", required=True)
def create(pkg: str) -> None:
    """
    Create a new PKGBUILD file for a pypi package.

    Args:
        pkg (str): Name of the pypi  package for which to create a PKGBUILD

    """
    createPKGBUILD(pypiPackage=pkg)


@cli.command()
def update() -> None:
    """
    update PKGBUILD file based to a pypi package.
    """
    updatePKGBUILD()


@cli.command()
@click.argument("pkg", required=True)
def showdeps(pkg: str) -> None:
    """
    Read and show pypi package dependencies.
    """
    readPyPiDeps(pypipackage=pkg)
