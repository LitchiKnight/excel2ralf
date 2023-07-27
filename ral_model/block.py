import sys
from base.default import *
from ral_model.register import Register

class Block:
    def __init__(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            print("[Error] block name must be string, please check!")
        self.__base_addr     = "\'h0"
        self.__bytes         = BLOCK_BYTES
        self.__register_list = []

    def set_base_addr(self, base_addr):
        if isinstance(base_addr, str):
            self.__base_addr = base_addr
        else:
            print(f"[Error] {self.get_block_name()}.base_addr must be string, please check!")
            sys.exit()
    
    def get_base_addr(self):
        return self.__base_addr

    def get_block_name(self):
        return self.__name

    def set_bytes(self, byte):
        if isinstance(byte, int):
            self.__bytes = byte
        else:
            print(f"[Error] {self.get_block_name()}.bytes must be int, please check!")
            sys.exit()

    def get_bytes(self):
        return self.__bytes

    def is_empty(self):
        return len(self.__register_list) == 0
    
    def has_register(self, name):
        for r in self.__register_list:
            if name == r.get_reg_name():
                return True
        return False

    def append_register(self, reg):
        if isinstance(reg, Register):
            self.__register_list.append(reg)
        else:
            print("[Error] invalid register object, please check!")
            sys.exit()

    def __get_real_addr(self, f_offset):
        offset = f_offset.replace("'h", "0x")
        base = self.__base_addr.replace("'h", "0x")
        real = hex(int(base, 16)+int(offset, 16))
        f_real = real.replace("0x", "'h")
        return f_real
    
    def gen_ral(self):
        ral = ""
        for r in self.__register_list:
            ral += r.gen_ral()
        ral += f"block {self.get_block_name()} {{\n\tbytes {self.get_bytes()};\n"
        for r in self.__register_list:
            ral += f"\tregister {r.get_reg_name()} @{self.__get_real_addr(r.get_offset())};\n"
        ral += "}\n"
        return ral
            