import sys
from base.enum import *
from ral_model.base import Base

class Memory(Base):
    def __init__(self, name):
        super().__init__(name)
        self.set_type(StorageType.MEM)
        self.__size   = 0
        self.__bits   = [0, 0]
        self.__access = "rw"

    # ================ size ================ #
    def set_size(self, size):
        self.__size = size

    def get_size(self):
        return self.__size

    # ================ bits ================ #
    def set_bits(self, bits):
        if not len(bits) == 2 or bits[0] < bits[1]:
            print(f"[Error] invalid value {bits} for memory {self.get_name()}.bits, please check!")
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
        ralf = f"memory {self.get_name()} {{\n\tbits {self.get_bit_range()};\n\tsize {self.__size};\n\taccess {self.__access};\n}}\n\n"
        return ralf