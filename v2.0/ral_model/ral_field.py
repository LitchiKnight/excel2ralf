from common.base import Base
from ral_model.ral_base import RalBase

class RalField(RalBase):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.reserved = (name == "reserved")
    
    def is_reserved(self):
        return self.name == 'reserved'

    def member_var_check(self):
        pass

    def gen_ralf_code(self):
        super().gen_ralf_code()
        ralf_code = f'\tfield {self.name} {{\n\t\tbits {self.bits};\n'
        if (not self.reserved):
            ralf_code += f'\t\taccess {self.access};\n\t\treset {self.reset};\n'
        ralf_code += '\t}}\n'
