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

    def gen_ralf_code(self) -> str:
        """Generate RALF code for the register."""
        super().gen_ralf_code()
        ralf_code = f'register {self.name} {{\n'
        for f in reversed(self.fields):
            ralf_code += f.gen_ralf_code()
        ralf_code += '}\n\n'
        return ralf_code