from typing import List
from common.base import Base
from ral_model.ral_base import RalBase
from ral_model.ral_register import RalRegister

class RalBlock(RalBase):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.baseaddr: str = ''
        self.bytes: str = ''
        self.registers: List[RalRegister] = []

    def add_register(self, register: RalRegister) -> None:
        """Add a register to the block."""
        self.registers.append(register)

    def get_latest_register(self) -> RalRegister:
        """Get the latest register added to the block."""
        if not self.registers:
            Base.error("There is no register in block, please check!")
        return self.registers[-1]
        
    def calc_bytes(self) -> None:
        """Calculate the byte size of the block based on its registers."""
        for r in self.registers:
            _bytes = str(int(r.width) // 8)
            if not self.bytes or int(self.bytes) > int(_bytes):
                self.bytes = _bytes

    def gen_ralf_code(self) -> str:
        """Generate RALF code for the block."""
        super().gen_ralf_code()

        ralf_code = ''
        self.calc_bytes()
        for r in self.registers:
          ralf_code += r.gen_ralf_code()
        ralf_code += f'block {self.name} {{\n\tbytes {self.bytes};\n'
        for r in self.registers:
          ralf_code += f'\tregister {r.name} ({r.name}) @{r.offset};\n'
        ralf_code += '}\n\n'
        return ralf_code
    


    