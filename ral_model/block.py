import sys
from base.macro import *
from base.enum import *
from ral_model.base import Base
from ral_model.register import Register

class Block:
    def __init__(self, name):
        self.__name      = name
        self.__bytes     = DEFAULT_BYTES
        self.__base_addr = "'h0"
        self.__item_list = []

    # ================ name ================ #
    def rename_block(self, name):
        self.__name = name

    def get_name(self):
        return self.__name

    # ================ bytes ================ #
    def set_bytes(self, bytes):
        self.__bytes = bytes

    def get_bytes(self):
        return self.__bytes

    def adapt_bytes(self):
        bytes = 0
        for item in self.__item_list:
            width = item.get_width()
            if int(width)//8 > bytes:
                bytes = int(width)//8
        self.set_bytes(bytes)

    # ================ base address ================ #
    def set_base_addr(self, addr):
        self.__base_addr = addr

    def get_base_addr(self):
        return self.__base_addr

    # ================ block item list ================ #
    def append_block_item(self, item):
        self.__item_list.append(item)

    def get_latest_block_item(self):
        if len(self.__item_list):
            return self.__item_list[-1]
        else:
            print(f"[Error] There is nothing in {self.get_name()} block, please check!")
            sys.exit()
    
    # ================ generate ralf code ================ #
    def gen_ralf_code(self):
        ralf = ""

        for item in self.__item_list:
            ralf += item.gen_ralf_code()
        
        ralf += f"block {self.get_name()} {{\n\tbytes {self.get_bytes()};\n"
        for item in self.__item_list:
            name = item.get_name()
            type = item.get_type()
            offset = item.get_offset()

            if type == StorageType.REG:
                ralf += f"\tregister {name} ({name}) @{offset};\n"
            elif type == StorageType.REG_ARR:
                ralf += f"\tregister {name}[{item.get_size()}] ({name}[%d]) @{offset};\n"
            elif type == StorageType.MEM:
                ralf += f"\tmemory {name} ({name}) @{offset};\n"
            else:
                print(f"[Error] Unrecognized storage type for {name}, please check!")
                sys.exit()
        ralf += "}\n\n"

        return ralf
            