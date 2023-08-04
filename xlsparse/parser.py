import os
import sys
import xlrd
import re
from base.macro import *
from base.enum import *
from ral_model.block import Block
from ral_model.register import Register
from ral_model.field import Field
from ral_model.memory import Memory

class XlsParser:
    def __init__(self):
        self.__table       = None
        self.__ral_model   = None
        self.__ral_code    = ""
        self.__module_name = ""

    def __parse_file_name(self, file_name):
        if re.match(FILE_NAME_PATTERN, file_name):
            self.__module_name = file_name.split("_project_")[1].split("_module_")[0]
        else:
            self.__module_name = DEFAULT_BLOCK_NAME

    def __read_xls(self, file_name):
        print(f"[Info] start convert {file_name}.")
        # try opening source file
        try:
            xls = xlrd.open_workbook(file_name)
        except:
            print(f"[Error] cannot open {file_name}, please check!")
            sys.exit()
        else:
            print(f"[Info] {file_name} will be parsed.")
        
        sheet_name = f"{self.__module_name}_module_reg_spec"
        if sheet_name in xls.sheet_names():
            self.__table = xls.sheet_by_name(sheet_name)
        else:
            print(f"[Error] cannot find target sheet {sheet_name}, please check!")
            sys.exit()

    def __parse_base_addr(self, row):
        col  = TableHeader.BASEADDRESS.value
        addr = self.__table.cell_value(row, col)
        addr = str(addr).strip()

        if addr and not re.match(BASE_ADDR_PATTERN, addr):
            print(f"[Error] line {row}: invalid BaseAddress value {addr}, please check!")
            sys.exit()
        else:
            return addr

    def __parse_type(self, row):
        col = TableHeader.TYPE.value
        type = self.__table.cell_value(row, col)
        type = str(type).strip()

        if type and not re.match(TYPE_PATTERN, type):
            print(f"[Error] line {row}: invalid Type value {type}, please check!")
            sys.exit()
        else:
            return type

    def __parse_offset(self, row):
        col    = TableHeader.OFFSETADDRESS.value
        offset = self.__table.cell_value(row, col)
        offset = str(offset).strip()

        if offset and not re.match(OFFSET_PATTERN, offset):
            print(f"[Error] line {row}: invalid OffsetAddress value {offset}, please check!")
            sys.exit()
        else:
            return offset

    def __parse_width(self, row):
        col = TableHeader.WIDTH.value
        width = self.__table.cell_value(row, col)
        if type(width) == float:
            i_width = int(width)
            if i_width == width:
                width = str(i_width)
            else:
                print(f"[Error] line {row}: invalid Width value {width}, please check!")
                sys.exit()
        width = width.strip()
        if width and not re.match(WIDTH_PATTERN, width):
            print(f"[Error] line {row}: invalid Width value {width}, please check!")
            sys.exit()
        else:
            return width

    def __parse_reg_name(self, row):
        col = TableHeader.REGNAME.value
        reg_name = self.__table.cell_value(row, col)
        reg_name = str(reg_name).strip()

        if reg_name and not re.match(NAME_PATTERN, reg_name):
            print(f"[Error] line {row}: invalid regName value {reg_name}, please check!")
            sys.exit()
        else:
            return reg_name

    def __parse_field_name(self, row):
        col = TableHeader.FIELDNAME.value
        field_name = self.__table.cell_value(row, col)
        field_name = str(field_name).strip()

        if field_name and not re.match(NAME_PATTERN, field_name):
            print(f"[Error] line {row}: invalid regName value {field_name}, please check!")
            sys.exit()
        else:
            return field_name

    def __parse_bits(self, row):
        col  = TableHeader.BITS.value
        bits = self.__table.cell_value(row, col)
        bits = str(bits).strip()

        if bits and not re.match(BITS_PATTERN, bits):
            print(f"[Error] line {row}: invalid Bits value {bits}, please check!")
            sys.exit()
        else:
            return bits

    def __parse_access(self, row):
        col    = TableHeader.ACCESS.value
        access = self.__table.cell_value(row, col)
        access = str(access).strip()

        if access and not re.match(ACCESS_PATTERN, access):
            print(f"[Error] line {row}: invalid Access value {access}, please check!")
            sys.exit()
        else:
            return access

    def __parse_reset(self, row):
        col   = TableHeader.RESETVALUE.value
        reset = self.__table.cell_value(row, col)
        reset = str(reset).strip()

        if reset and not re.match(RESET_PATTERN, reset):
            print(f"[Error] line {row}: invalid ResetValue value {reset}, please check!")
            sys.exit()
        else:
            return reset

    def __parse_desc(self, row):
        col = TableHeader.DESCRIPTION.value
        desc = self.__table.cell_value(row, col)
        desc = str(desc).strip()
        return desc

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

    def __format_addr(self, addr):
        addr = addr.replace("0x", "\'h")
        addr = addr.replace("0X", "\'h")
        return addr

    def __parse_reg(self, row):
        reg_name = self.__parse_reg_name(row)
        offset = self.__parse_offset(row)
        if not offset:
            print(f"[Error] OffsetAddress of register {reg_name} cannot be empty, please check!")
            sys.exit()
        width = self.__parse_width(row)
        if not width:
            print(f"[Error] Width of register {reg_name} cannot be empty, please check!")
            sys.exit()

        reg = Register(reg_name)
        reg.set_offset(self.__format_addr(offset))
        if re.match(REGARR_WIDTH_PATTERN, width):
            reg.set_reg_type(StorageType.REG_ARRAY)
            reg.set_reg_size(int(width.split("*")[1]))
            reg.set_width(int(width.split("*")[0]))
        else:
            reg.set_width(int(width))

        return reg

    def __parse_field(self, row, reg_name):
        field_name = self.__parse_field_name(row)
        bits = self.__parse_bits(row)
        if not bits:
            print(f"[Error] Bits of {reg_name}.{field_name} cannot be empty, please check!")
            sys.exit()
        bits = self.__formatting_bits(bits)
        access = self.__parse_access(row)
        if not access:
            print(f"[Error] Access of {reg_name}.{field_name} cannot be empty, please check!")
            sys.exit()
        reset = self.__parse_reset(row)
        if not reset:
            print(f"[Error] ResetValue of {reg_name}.{field_name} cannot be empty, please check!")
            sys.exit()

        field = Field(field_name)
        field.set_bits(bits)
        field.set_access(access)
        field.set_reset(reset)

        return field

    def __parse_mem(self, row):
        mem_name = self.__parse_reg_name(row)
        offset = self.__parse_offset(row)
        if not offset:
            print(f"[Error] OffsetAddress of memory {mem_name} cannot be empty, please check!")
            sys.exit()
        width = self.__parse_width(row)
        if not width:
            print(f"[Error] Width of memory {mem_name} cannot be empty, please check!")
            sys.exit()
        bits = self.__parse_bits(row)
        if not bits:
            print(f"[Error] Bits of memory {mem_name} cannot be empty, please check!")
            sys.exit()
        bits = self.__formatting_bits(bits)
        access = self.__parse_access(row)
        if not access:
            print(f"[Error] Access of memory {mem_name} cannot be empty, please check!")
            sys.exit()

        mem = Memory(mem_name)
        mem.set_offset(self.__format_addr(offset))
        mem.set_width(int(width.split("*")[0]))
        mem.set_size(width.split("*")[1])
        mem.set_bits(bits)
        mem.set_access(access)

        return mem

    def __parse_table(self):
        table = self.__table

        # create block instance
        block_name = f"{self.__module_name}" if self.__module_name else DEFAULT_BLOCK_NAME
        block = Block(block_name)
        self.__ral_model = block

        # table header double check
        for e in TableHeader:
            header_item = table.cell_value(0, e.value)
            if not header_item.upper() == e.name:
                print(f"[Error] unrecognized table header item {header_item}, please check!")
                sys.exit()

        # start parse table body
        row = 1
        state = ParserState.IDLE
        curr_base_addr = ""
        while True:
            if state == ParserState.IDLE: # IDLE state
                t = self.__parse_type(row)
                if t:
                    if StorageType.REG.name == t.upper():
                        base_addr = self.__parse_base_addr(row)
                        if base_addr:
                            curr_base_addr = self.__format_addr(base_addr)
                            block.add_reg_base_addr(curr_base_addr)
                        else:
                            print("[Error] base address of register cannot be empty, please check!")
                            sys.exit()
                        state = ParserState.PARSE_REG
                    elif StorageType.MEM.name == t.upper():
                        base_addr = self.__parse_base_addr(row)
                        if base_addr:
                            curr_base_addr = self.__format_addr(base_addr)
                            block.add_mem_base_addr(curr_base_addr)
                        else:
                            print("[Error] base address of memory cannot be empty, please check!")
                            sys.exit()
                        state = ParserState.PARSE_MEM
                else:
                    print("[Error] the value of the Type cannot be empty, please check!")
                    sys.exit()
            elif state == ParserState.PARSE_REG: # PARSE_REG state
                t = self.__parse_type(row)
                if t and not StorageType.REG.name == t.upper():
                    state = ParserState.IDLE
                    continue
                reg = self.__parse_reg(row)
                block.append_register(curr_base_addr, reg)
                state = ParserState.PARSE_FIELD
            elif state == ParserState.PARSE_MEM: # PARSE_MEM state
                t = self.__parse_type(row)
                if t and not StorageType.MEM.name == t.upper():
                    state = ParserState.IDLE
                    continue
                mem = self.__parse_mem(row)
                block.append_memory(curr_base_addr, mem)
                row += 1
            elif state == ParserState.PARSE_FIELD: # PARSE_FIELD state
                r = self.__parse_reg_name(row)
                reg = block.get_latest_register(curr_base_addr)
                if r and not reg.get_reg_name() == r:
                    state = ParserState.PARSE_REG
                    continue
                field = self.__parse_field(row, reg.get_reg_name())
                reg.append_field(field)
                row += 1
            elif state == ParserState.END: # END state
                break
            else:
                state = ParserState.IDLE

            # exit condition check
            if row == table.nrows:
                state = ParserState.END

    def __gen_ralf_code(self):
        self.__ral_code = self.__ral_model.gen_ralf_code()

    def set_module_name(self, name):
        if isinstance(name, str):
            self.__module_name = name
        else:
            print("[Error] module name must be string, please check!")

    def parse_xls(self, file_name):
        self.__parse_file_name(file_name)
        self.__read_xls(file_name)
        self.__parse_table()
        self.__gen_ralf_code()
        print(f"[Info] {self.__module_name} module register ral file convert done.")
    
    def get_ral(self):
        return self.__ral_code
