import sys
from base.const import *

class Field:
    def __init__(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            print("[Error] field name must be string, please check!")
        self.__bits   = 1
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
        if isinstance(bits, int):
            if bits > 0:
                self.__bits = bits
                return
            else:
                print(f"[Error] invalid value {bits} for {self.get_field_name()}.bits, please check!")
        else:
            print(f"[Error] {self.get_field_name()}.bits must be int, please check!")
        sys.exit()

    def get_bits(self):
        return self.__bits

    # ================ access ================ #
    def set_access(self, access):
        if isinstance(access, str):
            l_access = access.lower()
            if l_access in ACCESS_LIST:
                self.__access = l_access
                return
            else:
                print(f"[Error] invalid value {access} for {self.get_field_name()}.access, please check!")
        else:
            print(f"[Error] {self.get_field_name()}.access must be string, please check!")
        sys.exit()
    
    def get_access(self):
        return self.__access

    # ================ reset ================ #
    def set_reset(self, reset):
        if isinstance(reset, str):
            self.__reset = reset
            return
        else:
            print(f"[Error] {self.get_field_name()}.reset must be string, please check!")
        sys.exit()
    
    def get_reset(self):
        return self.__reset

    # ================ desc ================ #
    def set_desc(self, desc):
        self.__desc = desc

    def get_desc(self):
        return self.__desc

    def print(self):
        print(f"field {self.get_field_name()} {{\n\tbits {self.get_bits()}\n\taccess {self.get_access()}\n\treset {self.get_reset()}\n}}")

    def gen_ral(self):
        ral = f"\tfield {self.get_field_name()} {{\n\t\tbits {self.get_bits()};\n\t\taccess {self.get_access()};\n\t\treset {self.get_reset()};\n\t}}\n"
        return ral