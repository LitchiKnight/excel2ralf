import sys
from base.enum import *
from ral_model.field import Field
from ral_model.register import Register

class RegisterArray(Register):
    def __init__(self, name):
        super().__init__(name)
        self.set_type(StorageType.REG_ARR)
        self.__size = 0

    # ================ size ================ #
    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size