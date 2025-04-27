from typer import Typer

from odoo_toolkit.common import print_command_title

app = Typer()


@app.command()
def rebase(

) -> None:
    print_command_title(":arrow_right_hook: Rebase Multiverse Branches")
