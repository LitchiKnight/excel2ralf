from base.macro import *
from base.enum import *

class Base:
    def __init__(self, name):
        self.__name = name
        self.__type = StorageType.NONE
        self.__offset = "\'h0"
        self.__width = DEFAULT_WIDTH

    # ================ name ================ #
    def get_name(self):
        return self.__name

    # ================ type ================ #
    def set_type(self, type):
        self.__type = type

    def get_type(self):
        return self.__type

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
    
    # ================ generate ralf code ================ #
    def gen_ralf_code(self):
        pass