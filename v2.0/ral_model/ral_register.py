from common.base import Base
from ral_model.ral_base import RalBase

class RalRegister(RalBase):
  def __init__(self, name) -> None:
    super().__init__()
    self.name   = name
    self.offset = ''
    self.width  = ''
    self.fields = []

  def add_field(self, field):
    self.fields.append(field)

  def get_latest_field(self):
    if len(self.fields) <= 0:
      Base.error("there is no field in register, please check!")
    else:
      return self.fields[-1]

  def gen_ralf_code(self):
    super().gen_ralf_code()
    ralf_code = f'register {self.name} {{\n'
    for f in reversed(self.fields):
      ralf_code += f.gen_ralf_code()
    ralf_code += '}\n\n'
    return ralf_code