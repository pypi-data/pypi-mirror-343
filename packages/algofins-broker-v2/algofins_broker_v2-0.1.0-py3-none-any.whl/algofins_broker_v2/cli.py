"""Console script for algofins_broker_v2."""
import algofins_broker_v2

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for algofins_broker_v2."""
    console.print("Replace this message by putting your code into "
               "algofins_broker_v2.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
