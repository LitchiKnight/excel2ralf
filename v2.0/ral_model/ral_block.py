from common.base import Base
from ral_model.ral_base import RalBase
from ral_model.ral_register import RalRegister

class RalBlock(RalBase):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name
        self.registers = []

    def add_register(self, register: RalRegister):
        self.registers.append(register)

    def get_latest_register(self):
        if len(self.registers) <= 0:
            Base.error("there is no register in block, please check!")
        else:
            return self.registers[-1]
        
    def calc_bytes(self):
        pass

    def member_var_check(self):
        pass

    def gen_ralf_code(self):
        super().gen_ralf_code()

        ralf_code = ''
        for r in self.registers:
            ralf_code += r.gen_ralf_code()
        ralf_code += f'block {self.name} {{\n\tbytes {self.bytes};\n'
        for r in self.registers:
            ralf += f'\tregister {r.name} ({r.name}) @{r.offset};\n'
        ralf_code += '}\n\n'
        return ralf_code
    


    