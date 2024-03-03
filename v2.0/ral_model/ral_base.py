from abc import ABC, abstractmethod

class RalBase(ABC):
  def __init__(self) -> None:
    super().__init__()

  @abstractmethod
  def member_var_check(self):
    pass

  @abstractmethod
  def gen_ralf_code(self):
    self.member_var_check()