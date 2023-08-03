import sys
import re
from base.enum import *

class Memory:
    def __init__(self, name):
        self.__name   = name
        self.__type   = StorageType.MEM
        self.__offset = "\'h0"
        self.__width  = 32
        self.__size   = 0
        self.__bits   = [0, 0]
        self.__access = "rw"

    def get_mem_name(self):
        return self.__name

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

    # ================ size ================ #
    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    # ================ bits ================ #
    def set_bits(self, bits):
        if bits[0] < bits[1]:
            print(f"[Error] invalid value {bits} for {self.get_field_name()}.bits, please check!")
            sys.exit()
        self.__bits = bits

    def get_bits(self):
        return self.__bits

    def get_bit_range(self):
        return self.__bits[0] - self.__bits[1] + 1

    # ================ access ================ #
    def set_access(self, access):
        l_access = access.lower()
        if l_access == "rw" or l_access == "ro":
            self.__access = l_access
        else:
            print(f"[Error] memory {self.__name} doesn't support access type of {access}, please check!")
            sys.exit()

    def get_access(self):
        return self.__access

    # ================ generate ralf code ================ #
    def gen_ralf_code(self):
        ral = f"memory {self.__name} {{\n\tbits {self.get_bit_range()};\n\tsize {self.__size};\n\taccess {self.__access};\n}}\n\n"
        return ral