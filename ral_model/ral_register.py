from typing import List
from common.base import Base
from ral_model.ral_base import RalBase
from ral_model.ral_field import RalField

class RalRegister(RalBase):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name: str = name
        self.offset: str = ''
        self.width: str = ''
        self.reset: str = ''
        self.fields: List[RalField] = []

    def add_field(self, field: RalField) -> None:
        """Add a field to the register."""
        self.fields.append(field)

    def get_latest_field(self) -> RalField:
        """Get the latest field added to the register."""
        if not self.fields:
            Base.error("There is no field in register, please check!")
        return self.fields[-1]
    
    def verify_fields(self) -> None:
        """Verify if the fields are valid."""
        total_filed_bits = sum([int(f.bits) for f in self.fields])
        if total_filed_bits != int(self.width):
            Base.error(f"The sum of all field bits in register {self.name} is {total_filed_bits}, not equal to its bit width {self.width}, please check!")

    def gen_ralf_code(self) -> str:
        """Generate RALF code for the register."""
        super().gen_ralf_code()
        ralf_code = f'register {self.name} {{\n'
        for f in reversed(self.fields):
            ralf_code += f.gen_ralf_code()
        ralf_code += '}\n\n'
        return ralf_code