import sys
from base.macro import *
from base.enum import *
from ral_model.register import Register

class Block:
    def __init__(self, name):
        self.__name    = name
        self.__reg_map = {}
        self.__mem_map = {}
        self.__bytes   = DEFAULT_BLOCK_BYTES

    def __get_real_addr(self, base_addr, offset):
        offset    = offset.replace("'h", "0x")
        base_addr = base_addr.replace("'h", "0x")
        real      = hex(int(base_addr, 16)+int(offset, 16))
        f_real    = real.replace("0x", "'h")
        return f_real

    # ================ name ================ #
    def get_block_name(self):
        return self.__name

    # ================ register base address ================ #
    def add_reg_base_addr(self, addr):
        self.__reg_map.setdefault(addr, [])
    
    def get_reg_base_addr_list(self):
        return self.__reg_map.keys()

    # ================ memory base address ================ #
    def add_mem_base_addr(self, addr):
        self.__mem_map.setdefault(addr, [])

    def get_mem_base_addr_list(self):
        return self.__mem_map.keys()

    # ================ bytes ================ #
    def set_bytes(self, bytes):
        self.__bytes = bytes

    def get_bytes(self):
        return self.__bytes

    # ================ register map ================ #
    def append_register(self, base_addr, reg):
        if base_addr in self.__reg_map.keys():
            reg_list = self.__reg_map.get(base_addr)
            reg_list.append(reg)
        else:
            print(f"[Error] cannot find base address {base_addr} in block {self.get_block_name()}, please check!")
            sys.exit()

    def get_latest_register(self, base_addr):
        if base_addr in self.__reg_map.keys():
            reg_list = self.__reg_map.get(base_addr)
            if len(reg_list):
                return reg_list[-1]
            else:
                print(f"[Error] There is no register based on {base_addr} in {self.get_block_name()} block, please check!")
        else:
            print(f"[Error] cannot find register base address {base_addr} in {self.get_block_name()} block, please check!")
        sys.exit()

    # ================ memory map ================ #
    def append_memory(self, base_addr, mem):
        if base_addr in self.__mem_map.keys():
            mem_list = self.__mem_map.get(base_addr)
            mem_list.append(mem)
        else:
            print(f"[Error] cannot find memory base address {base_addr} in block {self.get_block_name()}, please check!")
            sys.exit()
    
    # ================ generate ralf code ================ #
    def gen_ralf_code(self):
        ral = ""
        for reg_list in self.__reg_map.values():
            for reg in reg_list:
                ral += reg.gen_ralf_code()

        for mem_list in self.__mem_map.values():
            for mem in mem_list:
                ral += mem.gen_ralf_code()
        
        ral += f"block {self.get_block_name()} {{\n\tbytes {self.get_bytes()};\n"
        for base_addr, reg_list in self.__reg_map.items():
            for reg in reg_list:
                if reg.get_reg_type() == StorageType.REG:
                    ral += f"\tregister {reg.get_reg_name()} @{self.__get_real_addr(base_addr, reg.get_offset())};\n"
                elif reg.get_reg_type() == StorageType.REG_ARRAY:
                    ral += f"\tregister {reg.get_reg_name()}[{reg.get_reg_size()}] @{self.__get_real_addr(base_addr, reg.get_offset())};\n"
        for base_addr, mem_list in self.__mem_map.items():
            for mem in mem_list:
                ral += f"\tmemory {mem.get_mem_name()} @{self.__get_real_addr(base_addr, mem.get_offset())};\n"
        ral += "}\n"
        return ral
            