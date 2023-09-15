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

    def get_name(self):
        return self.__name

    def is_reserved(self):
        return self.__name == "reserved"

    # ================ bits ================ #
    def set_bits(self, bits):
        if bits[0] < bits[1]:
            print(f"[Error] invalid value {bits} for {self.__name}.bits, please check!")
            sys.exit()
        self.__bits = bits

    def get_bits(self):
        return self.__bits
    
    def get_bit_range(self):
        return self.__bits[0] - self.__bits[1] + 1

    # ================ access ================ #
    def set_access(self, access):
        if (self.is_reserved()):
            print("[Error] cannot set access value for reserved field!")
            sys.exit()

        l_access = access.lower()
        if l_access in ACCESS_OPTIONS:
            self.__access = l_access
            return
        else:
            print(f"[Error] unrecognized value \"{access}\" for {self.__name}.access, please check!")
            sys.exit()
    
    def get_access(self):
        if (self.is_reserved()):
            print(f"[Error] cannot get access value from reserved field!")
            sys.exit()
        return self.__access

    # ================ reset ================ #
    def set_reset(self, reset):
        if (self.is_reserved()):
            print("[Error] cannot set reset value for reserved field!")
            sys.exit()
        self.__reset = reset
    
    def get_reset(self):
        if (self.is_reserved()):
            print(f"[Error] cannot get reset value from reserved field!")
            sys.exit()
        return self.__reset

    # ================ desc ================ #
    def set_desc(self, desc):
        self.__desc = desc

    def get_desc(self):
        return self.__desc

    # ================ generate ralf code ================ #
    def gen_ralf_code(self):
        if (not self.is_reserved()):
            ralf = f"\tfield {self.__name} {{\n\t\tbits {self.get_bit_range()};\n\t\taccess {self.__access};\n\t\treset {self.__reset};\n\t}}\n"
        else:
            ralf = f"\tfield {self.__name} {{\n\t\tbits {self.get_bit_range()};\n\t}}\n"
        return ralf