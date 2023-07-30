import os
import sys
import xlrd
import re
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
        except:
            print(f"[Error] cannot open {file_name}, please check!")
            sys.exit()
        else:
            print(f"[Info] {file_name} will be parsed.")

        self.__table = xls.sheet_by_name("reg_spec")

    def __formatting_bits(self, bits_s):
        symbol = ["[", "]", " "]
        for s in symbol:
            bits_s = bits_s.replace(s, "")
        bits_l = bits_s.split(":")
        end_bit = int(bits_l[0])
        start_bit = end_bit
        if len(bits_l) > 1:
            start_bit = int(bits_l[1])
        return [end_bit, start_bit]


    def __parse_addr(self, item, row, col):
        if item == "BaseAddress":
            pattern = "^(0x|0X)[a-fA-F0-9]{8}$"
        elif item == "OffsetAddress":
            pattern = "^(0x|0X)[a-fA-F0-9]{1,8}$"
        else:
            print(f"[Error] unknown table header \"{item}\" item, please check!")
            sys.exit()
        addr = self.__table.cell_value(row, col)
        addr = str(addr).strip()
        if addr and re.match(pattern, addr):
            return addr
        else:
            if not addr:
                print(f"[Error] empty element appear in \"{item}\" item, please check!")
            else:
                print(f"[Error] format error for \"{item}\" element, error value: \"{addr}\", please check!")
            sys.exit()

    def __parse_num(self, item, row, col):
        num = self.__table.cell_value(row, col)
        try:
            num = int(num)
        except:
            if not num:
                print(f"[Error] empty element appear in \"{item}\" item, please check!")
            else:
                print(f"[Error] format error for \"{item}\" element, error value: \"{num}\", please check!")
            exit()
        else:
            return num

    def __parse_name(self, item, row, col):
        pattern = "^[a-zA-Z0-9_]+$"
        name = self.__table.cell_value(row, col)
        name = str(name).strip()
        if not name or re.match(pattern, name):
            return name
        else:
            print(f"[Error] format error for \"{item}\" element, error value: \"{name}\", please check!")
            sys.exit()

    def __parse_bits(self, row, col):
        pattern = "^\[[0-9]+(:([0-9]+))?\]$"
        bits = self.__table.cell_value(row, col)
        bits = str(bits).strip()
        if bits and re.match(pattern, bits):
            return bits
        else:
            if not bits:
                print(f"[Error] empty element appear in \"Bits\" item, please check!")
            else:
                print(f"[Error] format error for Bits element, error value: \"{bits}\", please check!")
            sys.exit()

    def __parse_access(self, row, col):
        pattern = "^[a-zA-Z0-9]+$"
        access = self.__table.cell_value(row, col)
        access = str(access).strip()
        if access and re.match(pattern, access):
            return access
        else:
            if not access:
                print("[Error] empty element appear in \"Access\" item, please check!")
            else:
                print(f"[Error] format error for Access element, error value: \"{access}\", please check!")
            sys.exit()

    def __parse_reset(self, row, col):
        pattern = "(^[0-9]+\'b[0-1]+$)|(^[0-9]+\'h[a-fA-F0-9]+$)"
        reset = self.__table.cell_value(row, col)
        reset = str(reset).strip()
        if reset and re.match(pattern, reset):
            return reset
        else:
            if not reset:
                print("[Error] empty element appear in \"ResetValue\" item, please check!")
            else:
                print(f"[Error] format error for ResetValue element, error value: \"{reset}\", please check!")
            sys.exit()

    def __format_addr(self, addr):
        addr = addr.replace("0x", "\'h")
        addr = addr.replace("0X", "\'h")
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
        base_addr = self.__parse_addr("BaseAddress", 1, header["BaseAddress"])
        f_base_addr = self.__format_addr(base_addr)
        block.set_base_addr(f_base_addr)

        reg = None
        for r in range(table.nrows)[1:]:
            # parse register
            reg_name = self.__parse_name("RegName", r, header["RegName"])
            if reg_name:
                if block.has_register(reg_name):
                    print(f"[Error] register {reg_name} is already in block {block.get_block_name()}, please check!")
                    sys.exit()
                reg = Register(reg_name)
        
                site = self.__parse_num("Reg_site", r, header["Reg_site"])
                reg.set_site(int(site))

                offset = self.__parse_addr("OffsetAddress", r, header["OffsetAddress"])
                f_offset = self.__format_addr(offset)
                reg.set_offset(f_offset)

                width = self.__parse_num("Width", r, header["Width"])
                reg.set_width(int(width))

                block.append_register(reg)

            # parser field
            field_name = self.__parse_name("FieldName", r, header["FieldName"])
            if field_name:
                if reg.has_field(field_name):
                    print(f"[Error] field {field_name} is already in register {reg.get_reg_name()}, please check!")
                    sys.exit()
                field = Field(field_name)
            
                bits_str = self.__parse_bits(r, header["Bits"])
                bits = self.__formatting_bits(bits_str)
                field.set_bits(bits)

                access = self.__parse_access(r, header["Access"])
                field.set_access(access)

                reset = self.__parse_reset(r, header["ResetValue"])
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
