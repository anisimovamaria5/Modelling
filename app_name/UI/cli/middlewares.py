from functools import wraps
from typing import Any, Callable
import typer


def cli_handle_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            typer.echo(f"❌ Ошибка: {e}", err=True)
            raise typer.Exit(1)  
    return wrapper

