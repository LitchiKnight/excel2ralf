import sys
from base.const import *
from ral_model.field import Field

class Register:
    def __init__(self, name):
        self.__name       = name
        self.__site       = 0
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

    def is_empty(self):
        return len(self.__field_list) == 0
    
    def has_field(self, name):
        for f in self.__field_list:
            if f.get_field_name() == name:
                return True
        return False

    def gen_ral(self):
        ral = f"register {self.get_reg_name()} {{\n"
        for f in self.__field_list:
            ral += f.gen_ral()
        ral += "}\n\n"
        return ral
