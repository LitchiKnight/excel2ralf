from ral_model.ral_base import RalBase

class RalField(RalBase):
  def __init__(self, name: str) -> None:
    super().__init__()
    self.name     = name
    self.reserved = (name == 'reserved')
    self.bits     = ''
    self.access   = ''
    self.reset    = ''

  def gen_ralf_code(self):
    super().gen_ralf_code()
    ralf_code = f'\tfield {self.name} {{\n\t\tbits {self.bits};\n'
    if (not self.reserved):
      ralf_code += f'\t\taccess {self.access};\n\t\treset {self.reset};\n'
    ralf_code += '\t}\n'
    return ralf_code
