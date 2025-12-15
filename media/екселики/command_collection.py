import os
from pathlib import Path
import typer
from app_name.UI.cli.helpers import get_unique_filename
from app_name.UI.cli.cli_app import cli_app
from app_name.UI.sdk.factory import create_report_sdk



@cli_app.command("create_sample")
def create_collection_sample():
    """Создать пример файла для создания коллекции в формате xlsx"""
    try:
        sdk = create_report_sdk()
        output_file_name = get_unique_filename(
            base_path=Path(os.curdir),
            filename='Пример формы для создания файла коллекции.xlsx'
            )
        
        sdk.export_create_coll_report_sample(output_file_name)
        typer.echo(f"✅ Пример файла создан: {output_file_name}")
    except Exception as e:
        typer.echo(f"❌ Ошибка создания примера: {e}", err=True)
        raise typer.Exit(code=1)

@cli_app.command("create_from_file")
def create_collection_from_file(input_file: Path = typer.Argument(..., help="Путь к файлу с данными коллекции")):
    """Создать коллекцию из файла отчета"""
    try:
        sdk = create_report_sdk()
        result = sdk.create_coll_from_report_file(input_file)
        if result:
            typer.echo(f"✅ Коллекция успешно создана из файла: {input_file}")
        else:
            typer.echo(f"❌ Не удалось создать коллекцию из файла: {input_file}", err=True)
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Ошибка создания коллекции: {e}", err=True)
        raise typer.Exit(code=1)

@cli_app.command("export_collection")
def export_collection_to_file(collection_name: str = typer.Argument(..., help="Название коллекции для экспорта")):
    """Экспортировать коллекцию в файл отчета"""
    output_file = get_unique_filename(
        base_path=Path(os.curdir),
        filename=f'Коллекция {collection_name}.xlsx'
    )
    try:
        sdk = create_report_sdk()
        result = sdk.read_coll_report_view_by_title(collection_name, output_file)
        if result:
            typer.echo(f"✅ Коллекция '{collection_name}' экспортирована в: {output_file}")
        else:
            typer.echo(f"❌ Не удалось экспортировать коллекцию '{collection_name}'", err=True)
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Ошибка экспорта коллекции: {e}", err=True)
        raise typer.Exit(code=1)

@cli_app.command("import_records")
def import_records_from_file(
    input_file: Path = typer.Argument(..., help="Путь к файлу с записями"),
    replace: bool = typer.Option(False, "--replace", "-r", help="Заменить существующие записи")
):
    """Импортировать записи в коллекцию из файла отчета"""
    try:
        sdk = create_report_sdk()
        result = sdk.insert_records_by_coll_file(input_file, with_replace=replace)
        if result:
            action = "заменены" if replace else "добавлены"
            typer.echo(f"✅ Записи успешно {action} из файла: {input_file}")
        else:
            typer.echo(f"❌ Не удалось импортировать записи из файла: {input_file}", err=True)
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Ошибка импорта записей: {e}", err=True)
        raise typer.Exit(code=1)

@cli_app.command("remove_records")
def remove_records_from_file(
    input_file: Path = typer.Argument(..., help="Путь к файлу с записями для удаления")
):
    """Удалить записи из коллекции по файлу отчета"""
    try:
        sdk = create_report_sdk()
        result = sdk.remove_records_by_coll_file(input_file)
        if result:
            typer.echo(f"✅ Записи успешно удалены из коллекции по файлу: {input_file}")
        else:
            typer.echo(f"❌ Не удалось удалить записи по файлу: {input_file}", err=True)
            raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Ошибка удаления записей: {e}", err=True)
        raise typer.Exit(code=1)

@cli_app.command("show_config")
def show_config():
    """Показать текущую конфигурацию приложения"""
    try:
        from app_name.config import get_config
        config = get_config()
        typer.echo("🔧 Текущая конфигурация:")
        for field_name, field_value in config.model_dump().items():
            typer.echo(f"  {field_name}: {field_value}")
    except Exception as e:
        typer.echo(f"❌ Ошибка получения конфигурации: {e}", err=True)
        raise typer.Exit(code=1)