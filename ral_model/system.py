import sys
from base.macro import *
from base.enum import *
from ral_model.block import Block

class System:
    def __init__(self, name):
        self.__name       = name
        self.__bytes      = DEFAULT_BYTES
        self.__block_list = []

    def get_name(self):
        return self.__name

    def set_bytes(self, bytes):
        self.__bytes = bytes

    def get_bytes(self):
        return self.__bytes

    def append_block(self, block):
        self.__block_list.append(block)

    def gen_ralf_code(self):
        ralf = ""

        for block in self.__block_list:
            ralf += block.gen_ralf_code()

        ralf += f"system {self.get_name()} {{\n\tbytes {self.get_bytes()};\n"
        for block in self.__block_list:
            name = block.get_name()
            base_addr = block.get_base_addr()
            ralf += f"\tblock {name} @{base_addr};\n"
        ralf += "}\n"

        return ralf