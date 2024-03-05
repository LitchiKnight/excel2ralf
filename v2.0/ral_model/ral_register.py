from common.base import Base
from ral_model.ral_base import RalBase
from ral_model.ral_field import RalField

class RalRegister(RalBase):
  def __init__(self, name: str) -> None:
    super().__init__()
    self.name   = name
    self.offset = ''
    self.width  = ''
    self.reset  = ''
    self.fields = []

  def add_field(self, field: RalField) -> None:
    self.fields.append(field)

  def get_latest_field(self) -> RalField:
    if len(self.fields) <= 0:
      Base.error("there is no field in register, please check!")
    else:
      return self.fields[-1]

  def gen_ralf_code(self) -> str:
    super().gen_ralf_code()
    ralf_code = f'register {self.name} {{\n'
    for f in reversed(self.fields):
      ralf_code += f.gen_ralf_code()
    ralf_code += '}\n\n'
    return ralf_code