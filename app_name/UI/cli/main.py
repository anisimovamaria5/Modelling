import typer
from rich.console import Console
from app_name.UI.cli.cli_app import cli_app


def main():
    cli_app()

if __name__=='__main__':
    main()
