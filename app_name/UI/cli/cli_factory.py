import typer
from app_name.UI.cli import cli_commands

def create_cli_app():
    app = typer.Typer(
        name='dks',
        help='CLI для управления расчетами ДКС'
    )
    app.command('upload_excel')(cli_commands.upload_excel)
    app.command('save_to_db')(cli_commands.save_to_db)
    app.command('calc_modes')(cli_commands.calc_modes)
    app.command('calc_vfp')(cli_commands.calc_vfp)
    app.command('get_gdh')(cli_commands.get_gdh)
    app.command('get_default_params')(cli_commands.get_default_params)
    app.command('get_all_spch')(cli_commands.get_all_spch)
    app.command('get_bread_crumbs')(cli_commands.get_bread_crumbs)
    # app.command('get_companies')(cli_commands.get_companies)
    # app.command('get_fields')(cli_commands.get_fields)
    # app.command('get_dks')(cli_commands.get_dks)
    return app

cli_app = create_cli_app()