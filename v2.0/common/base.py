import sys
import time
from rich.console import Console

class Base:
  console = Console()

  def __init__(self) -> None:
    pass

  @classmethod
  def print(cls, msg):
    Base.console.print(msg)

  @classmethod
  def info(cls, msg):
    Base.console.print(f"[green bold]INFO:[/green bold] {msg}")

  @classmethod
  def warning(cls, msg):
    Base.console.print(f"[yellow bold]WARNING:[/yellow bold] {msg}")

  @classmethod
  def error(cls, msg):
    Base.console.print(f"[red bold]ERROR:[/red bold] {msg}")
    sys.exit()

  @classmethod
  def run_with_animation(cls, msg, func, *args):
    with Base.console.status(f"[green bold]{msg}"):
      time.sleep(1)
      try:
        return func(*args)
      except Exception as e:
        Base.error(e)