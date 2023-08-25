import sys
from base.enum import *
from ral_model.base import Base
from ral_model.field import Field

class Register(Base):
    def __init__(self, name):
        super().__init__(name)
        self.set_type(StorageType.REG)
        self.__field_list = []
        self.__rsv_cnt    = 0

    # ================ append field ================ #
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

    # ================ generate ralf code ================ #
    def gen_ralf_code(self):
        ralf = f"register {self.get_name()} {{\n"
        for f in reversed(self.__field_list):
            ralf += f.gen_ralf_code()
        ralf += "}\n\n"
        return ralf
