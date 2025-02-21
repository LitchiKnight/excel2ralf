from enum import Enum
import re

# Table header fields
class TableHeader(Enum):
    BASEADDRESS = 0
    TYPE = 1
    OFFSETADDRESS = 2
    REGNAME = 3
    WIDTH = 4
    REGRESETVALUE = 5
    BITS = 6
    FIELDNAME = 7
    ACCESS = 8
    FIELDRESETVALUE = 9
    DESCRIPTION = 10

# Field access options
class AccessOptions(Enum):
    RW = "rw"
    RO = "ro"
    WO = "wo"
    W1 = "w1"
    W1C = "w1c"
    RC = "rc"
    RS = "rs"
    WRC = "wrc"
    WRS = "wrs"
    WC = "wc"
    WS = "ws"
    WSRC = "wsrc"
    WCRS = "wcrs"
    W1S = "w1s"
    W1T = "w1t"
    W0C = "w0c"
    W0S = "w0s"
    W0T = "w0t"
    W1SRC = "w1src"
    W1CRS = "w1crs"
    W0SRC = "w0src"
    W0CRS = "w0crs"
    WOC = "woc"
    WOS = "wos"
    WO1 = "wo1"

# Register width options
VALID_WIDTH = [8, 16, 32]

# Patterns
BASEADDR_PATTERN = re.compile(r"^(0x|0X)[a-fA-F0-9]{4,8}$")
TYPE_PATTERN = re.compile(r"^reg$|^mem$")
OFFSET_PATTERN = re.compile(r"^(0x|0X)[a-fA-F0-9]{1,8}$")
NAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
REGARR_WIDTH_PATTERN = re.compile(r"^[1-9]+[0-9]*\*[1-9]+[0-9]*$")
WIDTH_PATTERN = re.compile(r"^[1-9]+[0-9]*$|^[1-9]+[0-9]*\*[1-9]+[0-9]*[k,M,G]?$")
BITS_PATTERN = re.compile(r"^\[[0-9]+(:([0-9]+))?\]$")
ACCESS_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")
RESET_PATTERN = re.compile(r"(^[1-9]+[0-9]*\'b[0-1]+$)|(^[1-9]+[0-9]*\'h[a-fA-F0-9]+$)")