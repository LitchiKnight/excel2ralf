import sys
from base.const import *
from ral_model.field import Field

class Register:
    def __init__(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            print("[Error] register name must be string, please check!")
        self.__site       = 0
        self.__offset     = "\'h0"
        self.__width      = 32
        self.__field_list = []
        self.__rsv_cnt = 0

    # ================ name ================ #
    def get_reg_name(self):
        return self.__name

    # ================ site ================ #
    def set_site(self, site):
        if isinstance(site, int):
            if site >= 0:
                self.__site = site
                return
            else:
                print(f"[Error] invalid value {site} for {self.get_reg_name()}.site, please check!")
        else:
            print(f"[Error] {self.get_reg_name()}.site must be int, please check!")

    def get_site(self):
        return self.__site

    # ================ offset ================ #
    def set_offset(self, offset):
        if isinstance(offset, str):
            self.__offset = offset
        else:
            #TODO: use regular expression later
            print(f"[Error] {self.get_reg_name()}.offset must be string, please check!")

    def get_offset(self):
        return self.__offset

    # ================ width ================ #
    def set_width(self, width):
        if isinstance(width, int):
            if width in VALID_WIDTH:
                self.__width = width
                return
            else:
                print(f"[Error] invalid value {width} for {self.get_reg_name()}.width, please check!")
        else:
            print(f"[Error] {self.get_reg_name()}.width must be int, please check!")                

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
