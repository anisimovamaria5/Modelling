import asyncio
import typer
from pathlib import Path
from app_name.UI.cli.cli_servise import *
from app_name.UI.cli.context_manager import cli_service_context
from app_name.infrastructure.adapters.xlsx_adapter import ExcelDataAdapter
from app_name.UI.cli.middlewares import cli_handle_errors
from rich.console import Console
from rich.table import Table
from rich import box
from rich.tree import Tree

console = Console()


@cli_handle_errors
def get_bread_crumbs():
    """Получить вложенное меню"""

    async def run():
        async with cli_service_context() as servise:
            return await servise.get_bread_crumbs()
        
    result = asyncio.run(run())
    
    if result:
        tree = Tree("🌍 [bold cyan]Структура ДКС[/bold cyan]", guide_style="bold bright_blue")

        def submenu_to_dict(submenu):
            """Рекурсивно преобразуем SubMenu в словарь"""
            result = {
                'name': submenu.name,
                'code': submenu.code
            }
            
            if submenu.children:
                if isinstance(submenu.children, list):
                    result['children'] = [submenu_to_dict(child) for child in submenu.children]
                else:
                    result['children'] = []
            else:
                result['children'] = []
            
            return result
        
        # Преобразуем все элементы
        converted_result = [submenu_to_dict(item) for item in result]        
        def add_to_tree(node, branch):
            """Рекурсивно добавляем узлы в дерево"""
            # Определяем иконку по уровню вложенности
            if 'children' in node and node['children']:
                for child in node['children']:
                    # Определяем тип по количеству вложенных детей
                    if 'children' in child and child['children']:
                        # Это месторождение (есть ДКС как дети)
                        child_branch = branch.add(f"⛰️ [bold green]{child['name']}[/bold green]")
                        add_to_tree(child, child_branch)
                    else:
                        # Это ДКС (нет детей)
                        branch.add(f"🏭 [white]{child['name']}[/white] (dks_code: {child.get('code', 'N/A')})")
            else:
                # Просто узел без детей
                branch.add(f"[grey]{node['name']} (Код: {node['code']})[/grey]")
        
        for company in converted_result:
            company_branch = tree.add(f"🏢 [bold yellow]{company['name']}[/bold yellow]")
            add_to_tree(company, company_branch)
        
        console.print(tree)
    
    return result 


@cli_handle_errors
def get_all_spch():
    """Получить список СПЧ из базы данных"""

    async def run():
        async with cli_service_context() as servise:
            return await servise.get_list_spch()

    result = asyncio.run(run())
    tree = Tree("📊 [bold cyan]СПЧ по компаниям[/bold cyan]", guide_style="bold blue")
    
    # Группируем данные
    grouped = {}
    for spch in result:
        company = spch.get('company_name', 'Неизвестная компания')
        field = spch.get('field_name', 'Неизвестное месторождение')
        dks = spch.get('dks_name', 'Неизвестный ДКС')
        
        if company not in grouped:
            grouped[company] = {}
        if field not in grouped[company]:
            grouped[company][field] = {}
        if dks not in grouped[company][field]:
            grouped[company][field][dks] = []
        
        grouped[company][field][dks].append(spch)
    
    # Строим дерево
    for company, fields in grouped.items():
        company_branch = tree.add(f"🏢 [bold yellow]{company}[/bold yellow]")
        
        for field, dks_dict in fields.items():
            field_branch = company_branch.add(f"⛰️ [bold green]{field}[/bold green]")
            
            for dks, spch_items in dks_dict.items():
                dks_branch = field_branch.add(f"🏭 [cyan]{dks}[/cyan]")
                
                for spch in spch_items:
                    dks_branch.add(f"📄 [white]СПЧ: {spch.get('name', 'Без названия')}[/white] (ID: {spch.get('id', 'N/A')})")

    console.print(tree)
    return result


@cli_handle_errors
def get_default_params(output: Path = typer.Argument(..., help="Путь к файлу с дефолтными параметрами")):
    setting_service = DefaultSettingService(output)
    data = setting_service.default_params()
    
    table = Table(
        title="[bold yellow]📋 ДЕФОЛТНЫЕ ПАРАМЕТРЫ[/bold yellow]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
        title_style="bold yellow"
    )
                
    table.add_column("Параметр", style="cyan", width=20)
    table.add_column("Значение", style="green", width=15)
    
    for key, value in data.items():
        table.add_row(key, str(value))
    
    console.print(table)
        
    return data


@cli_handle_errors
def upload_excel(
    deg: int = typer.Option(None, help="Степень полинома (по умолчанию: 4)"),
    k_value: float = typer.Option(None, help="Коэффициент политропы (по умолчанию: 1.31)"),
    press_conditional: float = typer.Option(None, help="Стандартная давление (по умолчанию: 0.101325)"),
    temp_conditional: float = typer.Option(None, help="Стандартная температура (по умолчанию: 283)"),
    file: Path = typer.Argument(..., help="Путь к файлу оцифрованными СПЧ"),
    output: Path = typer.Argument(..., help="Путь к файлу с безразмерными ГДХ")
):
    """Загрузить безразмерные ГДХ"""
    
    async def run():
        async with cli_service_context() as servise:
            return await servise.upload_excel(
                deg, k_value, press_conditional, temp_conditional, file
            )
        
    result = asyncio.run(run())

    if output:
        ExcelDataAdapter.save_result_in_excel(result, output)
        typer.echo(f"✅ Результат сохранен в {output}")
    else:
        typer.echo(f"❌ Не удалось сохранить", err=True)

    return result
  

@cli_handle_errors
def save_to_db(
    sheet_name: str = typer.Option(..., help="Имя листа в Excel 'Оцифрованные СПЧ'"),
    dks_code: str = typer.Option(..., help="Код ДКС из базы данных"),
    deg: int = typer.Option(None, help="Степень полинома (по умолчанию: 4)"),
    k_value: float = typer.Option(None, help="Коэффициент политропы (по умолчанию: 1.31)"),
    press_conditional: float = typer.Option(None, help="Стандартная давление (по умолчанию: 0.101325)"),
    temp_conditional: float = typer.Option(None, help="Стандартная температура (по умолчанию: 283)"),
    file: Path = typer.Argument(..., help="Путь к файлу с оцифрованными СПЧ"),
):
    """Сохранить СПЧ в базу данных"""
    
    async def run():
        async with cli_service_context() as servise:
            return await servise.save_to_db(
            sheet_name, dks_code,deg, k_value, press_conditional, temp_conditional, file
        )

    result = asyncio.run(run())

    if result:
        typer.echo(f"✅ Новая СПЧ добавлена в базу данных!", err=True)
    else:
        typer.echo(f"❌ Не удалось сохранить", err=True)
        
    return result


@cli_handle_errors
def calc_modes(
    deg: int = typer.Option(None, help="Степень полинома (по умолчанию: 4)"),
    conf_file: Path = typer.Argument(..., help="Путь к файлу компоновками"),
    modes_file: Path = typer.Argument(..., help="Путь к файлу с режимами (давления входа/выхода, расходы)"),
    bounds_file: Path = typer.Argument(..., help="Путь к файлу с граничными условиями"),
    output: Path = typer.Argument(..., help="Путь к файлу с посчитанными режимами")
):
    """Получить прогнозные режимы ДКС"""
    
    async def run():
        async with cli_service_context() as servise:
            return await servise.calculate_modes(
                conf_file, modes_file, bounds_file, deg
            )
        
    result = asyncio.run(run())

    if output:
        ExcelDataAdapter.save_result_in_excel(result, output)
        typer.echo(f"✅ Результат сохранен в {output}")
    else:
        typer.echo(f"❌ Не удалось сохранить", err=True)

    return result
    

@cli_handle_errors
def calc_vfp(
    deg: int = typer.Option(None, help="Степень полинома (по умолчанию: 4)"),
    conf_file: Path = typer.Argument(..., help="Путь к файлу компоновками"),
    table_params_file: Path = typer.Argument(..., help="Путь к файлу с режимами (давления выхода, расходы)"),
    bounds_file: Path = typer.Argument(..., help="Путь к файлу с граничными условиями"),
    output: Path = typer.Argument(..., help="Путь к файлу с таблицей VFP")
):
    """Получить таблицу VFP"""
    
    async def run():
        async with cli_service_context() as servise:
            return await servise.calculate_vfp(
                conf_file, table_params_file, bounds_file, deg
            )
        
    result = asyncio.run(run())
    
    if output:
        ExcelDataAdapter.save_result_in_excel(result, output)
        typer.echo(f"✅ Результат сохранен в {output}")
    else:
        typer.echo(f"❌ Не удалось сохранить", err=True)

    return result
    

@cli_handle_errors
def get_gdh(
    id: int = typer.Option(None, help="Степень полинома (по умолчанию: 4)"),
    output: Path = typer.Argument(..., help="Путь к файлу с размерной ГДХ")
):
    """Получить размерную ГДХ"""

    async def run():
        async with cli_service_context() as servise:
            return await servise.get_gdh_by_id(id)
        
    result = asyncio.run(run())
    
    if output:
        ExcelDataAdapter.save_result_in_excel(result, output)
        typer.echo(f"✅ Результат сохранен в {output}")
    else:
        typer.echo(f"❌ Не удалось сохранить", err=True)

    return result



@cli_handle_errors
def get_companies():
    """Получить список всех компаний"""

    async def run():
        async with cli_service_context() as servise:
            companies = await servise.get_all_companies()
            res = []
            for company in companies:
                res.append({
                    'id': company.id,
                    'code': company.code,
                    'name': company.name,
                })
            return res
        
    result = asyncio.run(run())

    if result:
        typer.echo(f"Список компаний: {result}", err=True)
        
    return result
    

@cli_handle_errors
def get_fields(company_code: str = typer.Argument(..., help="Код компании из базы данных")):
    """Получить список месторождений"""

    async def run():
        async with cli_service_context() as servise:
            fields = await servise.get_list_fields(company_code)
            res = []
            for field in fields:
                res.append({
                    'id': field.id,
                    'code': field.code,
                    'name': field.name,
                })
            return res
        
    result = asyncio.run(run())
    
    if result:
        typer.echo(f"Список месторождений в выбранной компании: {result}", err=True)

    return result
    

@cli_handle_errors
def get_dks(field_code: str = typer.Option(..., help="Код месторождения из базы данных")):
    """Получить список ДКС"""

    async def run():
        async with cli_service_context() as servise:
            dkd_all = await servise.get_list_dks(field_code)
            res = []
            for dkd in dkd_all:
                res.append({
                    'id': dkd.id,
                    'code': dkd.code,
                    'name': dkd.name,
                })
            return res
        
    result = asyncio.run(run())
    
    if result:
        typer.echo(f"Список ДКС в выбранном месторождении: {result}", err=True)

    return result
    
