import os
import sys
import xlrd
import re
from base.macro import *
from base.enum import *
from ral_model.field import Field
from ral_model.base import Base
from ral_model.register import Register
from ral_model.register_array import RegisterArray
from ral_model.memory import Memory
from ral_model.block import Block
from ral_model.system import System
 
class ExcelParser:
    def __init__(self):
        self.__table       = None
        self.__module_name = ""
        self.__block_list  = []
        self.__ral_list    = {}

    def __parse_excel(self, f_name):
        print(f"[Info] start parsing {f_name}.")
        # try opening source file
        try:
            excel = xlrd.open_workbook(f_name)
        except:
            print(f"[Error] cannot open {f_name}, please check!")
            sys.exit()

        self.__table = excel.sheets()[1]
        module_name = excel.sheet_names()[1]
        self.set_module_name(module_name)

    # ================ parse table items ================ #
    def __parse_base_addr(self, row):
        col  = TableHeader.BASEADDRESS.value
        addr = self.__table.cell_value(row, col)
        addr = str(addr).strip()

        if addr and not re.match(BASE_ADDR_PATTERN, addr):
            print(f"[Error] line{row+1}: invalid BaseAddress value {addr}, please check!")
            sys.exit()
        else:
            return addr

    def __parse_type(self, row):
        col = TableHeader.TYPE.value
        type = self.__table.cell_value(row, col)
        type = str(type).strip()

        if type and not re.match(TYPE_PATTERN, type):
            print(f"[Error] line{row+1}: invalid Type value {type}, please check!")
            sys.exit()
        else:
            return type

    def __parse_offset(self, row):
        col    = TableHeader.OFFSETADDRESS.value
        offset = self.__table.cell_value(row, col)
        offset = str(offset).strip()

        if offset and not re.match(OFFSET_PATTERN, offset):
            print(f"[Error] line{row+1}: invalid OffsetAddress value {offset}, please check!")
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
                print(f"[Error] line{row+1}: invalid Width value {width}, please check!")
                sys.exit()
        width = width.strip()
        if width and not re.match(WIDTH_PATTERN, width):
            print(f"[Error] line{row+1}: invalid Width value {width}, please check!")
            sys.exit()
        else:
            return width

    def __parse_reg_name(self, row):
        col = TableHeader.REGNAME.value
        reg_name = self.__table.cell_value(row, col)
        reg_name = str(reg_name).strip()

        if reg_name and not re.match(NAME_PATTERN, reg_name):
            print(f"[Error] line{row+1}: invalid regName value {reg_name}, please check!")
            sys.exit()
        else:
            return reg_name

    def __parse_field_name(self, row):
        col = TableHeader.FIELDNAME.value
        field_name = self.__table.cell_value(row, col)
        field_name = str(field_name).strip()

        if field_name and not re.match(NAME_PATTERN, field_name):
            print(f"[Error] line{row+1}: invalid regName value {field_name}, please check!")
            sys.exit()
        else:
            return field_name

    def __parse_bits(self, row):
        col  = TableHeader.BITS.value
        bits = self.__table.cell_value(row, col)
        bits = str(bits).strip()

        if bits and not re.match(BITS_PATTERN, bits):
            print(f"[Error] line{row+1}: invalid Bits value {bits}, please check!")
            sys.exit()
        else:
            return bits

    def __parse_access(self, row):
        col    = TableHeader.ACCESS.value
        access = self.__table.cell_value(row, col)
        access = str(access).strip()

        if access and not re.match(ACCESS_PATTERN, access):
            print(f"[Error] line{row+1}: invalid Access value {access}, please check!")
            sys.exit()
        else:
            return access

    def __parse_reset(self, row):
        col   = TableHeader.RESETVALUE.value
        reset = self.__table.cell_value(row, col)
        reset = str(reset).strip()

        if reset and not re.match(RESET_PATTERN, reset):
            print(f"[Error] line{row+1}: invalid ResetValue value {reset}, please check!")
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
        addr = addr.replace("0x", "\'h") # 0x -> 'h
        addr = addr.replace("0X", "\'h") # 0X -> 'h
        return addr

    def __parse_reg(self, row):
        reg_name = self.__parse_reg_name(row)
        offset   = self.__parse_offset(row)
        width    = self.__parse_width(row)

        # register property check
        try:
            if not offset:
                raise Exception(f"[Error] OffsetAddress of register {reg_name} cannot be empty, please check!")
            if not width:
                raise Exception(f"[Error] Width of register {reg_name} cannot be empty, please check!")
        except Exception as e:
            print(e)
            sys.exit()

        reg = None
        if re.match(REGARR_WIDTH_PATTERN, width):
            reg = RegisterArray(reg_name)
            reg.set_offset(self.__format_addr(offset))
            reg.set_width(int(width.split("*")[0]))
            reg.set_size(int(width.split("*")[1]))
        else:
            reg = Register(reg_name)
            reg.set_offset(self.__format_addr(offset))
            reg.set_width(int(width))

        return reg

    def __parse_field(self, row, reg_name):
        field_name = self.__parse_field_name(row)
        bits       = self.__parse_bits(row)
        if (not field_name == "reserved"):
            access = self.__parse_access(row)
            reset  = self.__parse_reset(row)

        # field property check
        try:
            if not field_name:
                raise Exception(f"[Error] line{row+1}: occur an empty FieldName, please check!")
            if not bits:
                raise Exception(f"[Error] Bits of {reg_name}.{field_name} cannot be empty, please check!")
            if (not field_name == "reserved" and not access):
                raise Exception(f"[Error] Access of {reg_name}.{field_name} cannot be empty, please check!")
            if (not field_name == "reserved" and not reset):
                raise Exception(f"[Error] ResetValue of {reg_name}.{field_name} cannot be empty, please check!")
        except Exception as e:
            print(e)
            sys.exit()
        
        field = Field(field_name)
        bits = self.__formatting_bits(bits)
        field.set_bits(bits)
        if (not field_name == "reserved"):
            field.set_access(access)
            field.set_reset(reset)

        return field

    def __parse_mem(self, row):
        mem_name = self.__parse_reg_name(row)
        offset   = self.__parse_offset(row)
        width    = self.__parse_width(row)
        bits     = self.__parse_bits(row)
        access   = self.__parse_access(row)

        try:
            if not offset:
                raise Exception(f"[Error] OffsetAddress of memory {mem_name} cannot be empty, please check!")
            if not width:
                raise Exception(f"[Error] Width of memory {mem_name} cannot be empty, please check!")
            if not bits:
                raise Exception(f"[Error] Bits of memory {mem_name} cannot be empty, please check!")
            if not access:
                raise Exception(f"[Error] Access of memory {mem_name} cannot be empty, please check!")
        except Exception as e:
            print(e)
            sys.exit()

        mem = Memory(mem_name)
        mem.set_offset(self.__format_addr(offset))
        mem.set_width(int(width.split("*")[0]))
        mem.set_size(width.split("*")[1])
        bits = self.__formatting_bits(bits)
        mem.set_bits(bits)
        mem.set_access(access)

        return mem

    def __parse_table(self):
        table = self.__table

        # table header double check
        for e in TableHeader:
            header_item = table.cell_value(0, e.value)
            if not header_item.upper() == e.name:
                print(f"[Error] unrecognized table header item {header_item}, please check!")
                sys.exit()

        # start parse table body
        row = 1
        state = ParserState.IDLE
        pre_state = state
        while True:
            # fetch latest block object
            block = self.__block_list[-1] if len(self.__block_list) else None
            # FSM
            if state == ParserState.IDLE: # IDLE state
                # create block
                block_name = f"{self.__module_name}"
                block = Block(block_name)
                # parse base address
                base_addr = self.__parse_base_addr(row)
                block.set_base_addr(self.__format_addr(base_addr))
                # store block object
                self.__block_list.append(block)
                # update previous state and next state
                pre_state, state = state, ParserState.PARSE_BLOCK
            elif state == ParserState.PARSE_BLOCK:
                if pre_state.value >= state.value:
                    base_addr = self.__parse_base_addr(row)
                    if base_addr:
                        pre_state, state = state, ParserState.IDLE
                        continue
                # parse type
                type = self.__parse_type(row)
                if not type:
                    print("[Error] the value of the Type cannot be empty, please check!")
                    sys.exit()
                # check storage type
                if StorageType.REG.name == type.upper():
                    pre_state, state = state, ParserState.PARSE_REG # set FSM next state as PARSE_REG
                if StorageType.MEM.name == type.upper():
                    pre_state, state = state, ParserState.PARSE_MEM # set FSM next state as PARSE_MEM
            elif state == ParserState.PARSE_REG:
                if pre_state.value >= state.value:
                    type = self.__parse_type(row)
                    if type:
                        pre_state, state = state, ParserState.PARSE_BLOCK # next state return to PARSE_BLOCK
                        continue
                reg = self.__parse_reg(row)
                block.append_block_item(reg)
                pre_state, state = state, ParserState.PARSE_FIELD # set FSM next state as PARSE_FIELD
            elif state == ParserState.PARSE_MEM:
                if pre_state.value >= state.value:
                    type = self.__parse_type(row)
                    if type:
                        pre_state, state = state, ParserState.PARSE_BLOCK # next state return to PARSE_BLOCK
                        continue
                mem = self.__parse_mem(row)
                block.append_block_item(mem)
                pre_state = state
                row += 1
            elif state == ParserState.PARSE_FIELD:
                if pre_state.value >= state.value:
                    reg_name = self.__parse_reg_name(row)
                    if reg_name:
                        pre_state, state = state, ParserState.PARSE_REG # next state return to PARSE_REG
                        continue
                reg = block.get_latest_block_item()
                field = self.__parse_field(row, reg.get_name())
                reg.append_field(field)
                pre_state = state
                row += 1
            elif state == ParserState.END: # END state
                break
            else:
                pre_state, state = state, ParserState.IDLE # next state return to IDLE

            # exit condition check
            if row == table.nrows:
                state = ParserState.END

    def __adapt_block_name(self):
        def do_rename(block):
            block_name = block.get_name()
            base_addr  = block.get_base_addr()
            base_addr  = base_addr.replace("\'h", "0x")
            block.rename_block(f"{block_name}_{base_addr}")

        for block in self.__block_list:
            block_name = block.get_name()
            filter_list = list(filter(lambda b: b.get_name() == block_name, self.__block_list))
            if len(filter_list) > 1:
                for item in filter_list:
                    do_rename(item)

    # ================ public functions ================ #
    def set_module_name(self, name):
        self.__module_name = name

    def get_module_name(self):
        return self.__module_name

    def parse_excel_file(self, path):
        cwd = os.getcwd()
        abs = os.path.abspath(path)
        dir = os.path.dirname(abs)
        f_name = os.path.basename(abs)

        os.chdir(dir)
        if not re.match(FILE_NAME_PATTERN, f_name):
            print(f"[Error] invalid file name \'{f_name}\', it must be .xls or .xlsx file, please check!")
            sys.exit()
        self.__parse_excel(f_name)
        self.__parse_table()
        os.chdir(cwd)

    def gen_module_ralf(self):
        self.__adapt_block_name()
        for block in self.__block_list:
            block.adapt_bytes()
            base_addr = block.get_base_addr()
            self.__ral_list.setdefault(base_addr, block.gen_ralf_code())

    def gen_system_ralf(self):
        system = System(DEFAULT_SYSTEM_NAME)
        self.__adapt_block_name()
        for block in self.__block_list:
            block.adapt_bytes()
            system.append_block(block)
        self.__ral_list.setdefault("\'h0", system.gen_ralf_code())

    def get_ralf(self):
        return self.__ral_list
