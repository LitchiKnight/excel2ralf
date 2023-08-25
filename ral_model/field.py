import sys
from base.macro import *

class Field:
    def __init__(self, name):
        self.__name   = name
        self.__bits   = [0, 0]
        self.__access = "rw"
        self.__reset  = "1'b0"
        self.__desc   = ""

    # ================ field ================ #
    def rename_field(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            print("[Error] field name must be string, please check!")        

    def get_field_name(self):
        return self.__name

    # ================ bits ================ #
    def set_bits(self, bits):
        if bits[0] < bits[1]:
            print(f"[Error] invalid value {bits} for {self.get_field_name()}.bits, please check!")
            sys.exit()
        self.__bits = bits

    def get_bits(self):
        return self.__bits
    
    def get_bit_range(self):
        return self.__bits[0] - self.__bits[1] + 1

    # ================ access ================ #
    def set_access(self, access):
        l_access = access.lower()
        if l_access in ACCESS_OPTIONS:
            self.__access = l_access
            return
        else:
            print(f"[Error] unrecognized value \"{access}\" for {self.get_field_name()}.access, please check!")
            sys.exit()
    
    def get_access(self):
        return self.__access

    # ================ reset ================ #
    def set_reset(self, reset):
        self.__reset = reset
    
    def get_reset(self):
        return self.__reset

    # ================ desc ================ #
    def set_desc(self, desc):
        self.__desc = desc

    def get_desc(self):
        return self.__desc

    # ================ generate ralf code ================ #
    def gen_ralf_code(self):
        ralf = f"\tfield {self.__name} {{\n\t\tbits {self.get_bit_range()};\n\t\taccess {self.__access};\n\t\treset {self.__reset};\n\t}}\n"
        return ralf