from typing import List
from common.base import Base
from ral_model.ral_base import RalBase
from ral_model.ral_block import RalBlock

class RalSystem(RalBase):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.bytes: str = ''
        self.blocks: List[RalBlock] = []

    def add_block(self, block: RalBlock) -> None:
        """Add a block to the system."""
        self.blocks.append(block)
  
    def get_latest_block(self) -> RalBlock:
        """Get the latest block added to the system."""
        if not self.blocks:
            Base.error("There is no block in system, please check!")
        return self.blocks[-1]

    def calc_bytes(self) -> None:
        """Calculate the byte size of the system based on its blocks."""
        for b in self.blocks:
            _bytes = str(int(b.bytes))
            if not self.bytes or int(self.bytes) < int(_bytes):
                self.bytes = _bytes

    def gen_ralf_code(self) -> str:
        """Generate RALF code for the system."""
        super().gen_ralf_code()

        ralf_code = ''
        self.calc_bytes()
        for b in self.blocks:
            ralf_code += b.gen_ralf_code()
        ralf_code += f'system {self.name} {{\n\tbytes {self.bytes};\n'
        for b in self.blocks:
            ralf_code += f'\tblock {b.name} @{b.baseaddr};\n'
        ralf_code += '}\n'
        return ralf_code