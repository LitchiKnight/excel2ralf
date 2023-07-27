import os
import sys
import xlrd
import json
from base.default import *
from ral_model.block import Block
from ral_model.register import Register
from ral_model.field import Field

class Parser:
    def __init__(self):
        self.__table = None
        self.__ral_model = None
        self.__ral = ""
        self.__module_name = ""

    def set_module_name(self, name):
        if isinstance(name, str):
            self.__module_name = name
        else:
            print("[Error] module name must be string, please check!")

    def __read_xls(self, file_path):
        file_name = os.path.basename(file_path)
        print(f"[Info] start convert {file_name}.")

        # try opening source file
        try:
            xls = xlrd.open_workbook(file_path)
        except OS[Error]:
            print(f"[Error] cannot open {file_name}, please check!")
            sys.exit()
        else:
            print(f"[Info] {file_name} will be parsed.")

        self.__table = xls.sheet_by_name("reg_spec")

    def __get_bits_range(self, bits):
        symbol = ["[", "]", " "]
        for s in symbol:
            bits = bits.replace(s, "")
        range = bits.split(":")
        end_bit = int(range[0])
        start_bit = end_bit
        if len(range) > 1:
            start_bit = int(range[1])
        return end_bit - start_bit + 1

    def __format_addr(self, addr):
        addr = addr.replace(" ", "")
        addr = addr.replace("0x", "\'h")
        return addr

    def __parse_table(self):
        table = self.__table
        block_name = f"{self.__module_name}" if self.__module_name else BLOCK_NAME
        block = Block(block_name)
        self.__ral_model = block

        header = {}
        for i in range(table.ncols):
            header.setdefault(table.cell_value(0, i), i)
        
        # get base address in line 1
        base_addr = table.cell_value(1, header["BaseAddress"])
        f_base_addr = self.__format_addr(base_addr)
        block.set_base_addr(f_base_addr)

        reg = None
        for r in range(table.nrows)[1:]:
            # parse register
            reg_name = table.cell_value(r, header["RegName"])
            if reg_name:
                if block.has_register(reg_name):
                    print(f"[Error] register {reg_name} is already in block {block.get_block_name()}, please check!")
                    sys.exit()
                reg = Register(reg_name)
        
                site = table.cell_value(r, header["Reg_site"])
                if site:
                    reg.set_site(int(site))

                offset = table.cell_value(r, header["OffsetAddress"])
                f_offset = self.__format_addr(offset)
                if offset:
                    reg.set_offset(f_offset)

                width = table.cell_value(r, header["Width"])
                if width:
                    reg.set_width(int(width))

                block.append_register(reg)
            
            # parser field
            field_name = table.cell_value(r, header["FieldName"])
            if field_name:
                if reg.has_field(field_name):
                    print(f"[Error] field {field_name} is already in register {reg.get_reg_name()}, please check!")
                    sys.exit()
                field = Field(field_name)
            
                bits = table.cell_value(r, header["Bits"])
                if bits:
                    bits_range = self.__get_bits_range(bits)
                    field.set_bits(bits_range)

                access = table.cell_value(r, header["Access"])
                if access:
                    field.set_access(access)

                reset = table.cell_value(r, header["ResetValue"])
                if reset:
                    field.set_reset(reset)

                reg.append_field(field)

    def __gen_ral(self):
        self.__ral = self.__ral_model.gen_ral()

    def xls2ralf(self, file_path):
        self.__read_xls(file_path)
        self.__parse_table()
        self.__gen_ral()
        print(f"[Info] {self.__module_name} module register ral file convert done.")
    
    def get_ral(self):
        return self.__ral
