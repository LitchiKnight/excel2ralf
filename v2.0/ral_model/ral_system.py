from common.base import Base
from ral_model.ral_base import RalBase
from ral_model.ral_block import RalBlock

class RalSystem(RalBase):
  def __init__(self, name: str) -> None:
    super().__init__()
    self.name   = name
    self.bytes  = ''
    self.blocks = []

  def add_block(self, block: RalBlock) -> None:
    self.blocks.append(block)
  
  def get_latest_block(self) -> RalBlock:
    if len(self.blocks) <= 0:
      Base.error("there is no block in system, please check!")
    else:
      return self.blocks[-1]

  def calc_bytes(self) -> None:
    pass

  def gen_ralf_code(self) -> str:
    super().gen_ralf_code()

    ralf_code = ''
    self.calc_bytes()
    for b in self.blocks:
      ralf_code += b.gen_ralf_code()
    ralf_code += f'system {self.name} {{\n\tbytes {self.bytes};\n'
    for b in self.blocks:
      b_name = b.name
      b_addr = b.addr
      ralf_code += f'\tblock {b_name} @{b_addr};\n'
    ralf_code += '}\n'
    return ralf_code