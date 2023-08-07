import sys
import re
from base.macro import *
from base.enum import *
from ral_model.field import Field

class Register:
    def __init__(self, name):
        self.__name       = name
        self.__type       = StorageType.REG
        self.__size       = 1
        self.__offset     = "\'h0"
        self.__width      = 32
        self.__field_list = []
        self.__rsv_cnt    = 0

    # ================ name ================ #
    def get_reg_name(self):
        return self.__name

    # ================ site ================ #
    def set_site(self, site):
        self.__site = site

    def get_site(self):
        return self.__site

    # ================ offset ================ #
    def set_offset(self, offset):
        self.__offset = offset

    def get_offset(self):
        return self.__offset

    # ================ width ================ #
    def set_width(self, width):
        self.__width = width

    def get_width(self):
        return self.__width

    # ================ type ================ #
    def set_reg_type(self, type):
        self.__type = type

    def get_reg_type(self):
        return self.__type
    
    # ================ size ================ #
    def set_reg_size(self, size):
        self.__size = size

    def get_reg_size(self):
        return self.__size

    def append_field(self, field):
        if isinstance(field, Field):
            field_name = field.get_field_name()
            if field_name == "reserved" or field_name == "rsv":
                new_name = f"{field_name}_{str(self.__rsv_cnt)}"
                field.rename_field(new_name)
                self.__rsv_cnt += 1
            self.__field_list.append(field)
            return
        else:
            print("[Error] invalid field object, please check!")
        sys.exit()

    def has_field(self, name):
        for f in self.__field_list:
            if f.get_field_name() == name:
                return True
        return False

    def gen_ralf_code(self):
        ral = f"register {self.__name} {{\n"
        for f in reversed(self.__field_list):
            ral += f.gen_ralf_code()
        ral += "}\n\n"
        return ral
