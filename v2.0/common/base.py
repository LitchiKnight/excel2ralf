from typing import Callable, Any
from rich.console import Console
import time
import sys

class Base:
    console = Console()

    def __init__(self) -> None:
        pass

    @classmethod
    def _log(cls, level: str, color: str, msg: str) -> None:
        cls.console.print(f"[{color} bold]{level.upper()}:[/{color} bold] {msg}")

    @classmethod
    def print(cls, msg: str) -> None:
        cls.console.print(msg)

    @classmethod
    def info(cls, msg: str) -> None:
        cls._log("INFO", "green", msg)

    @classmethod
    def warning(cls, msg: str) -> None:
        cls._log("WARNING", "yellow", msg)

    @classmethod
    def error(cls, msg: str, exit_code: int = 1) -> None:
        cls._log("ERROR", "red", msg)
        sys.exit(exit_code)

    @classmethod
    def run_with_animation(cls, msg: str, func: Callable[..., Any], *args: Any) -> Any:
        with cls.console.status(f"[green bold]{msg}"):
            time.sleep(0.5)
            try:
                result = func(*args)
                time.sleep(0.5)
                return result
            except Exception as e:
                cls.error(e)