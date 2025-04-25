from .kernel import *
from .click import cli, showNameAndVersion


def main() -> None:
    showNameAndVersion()
    cli()
