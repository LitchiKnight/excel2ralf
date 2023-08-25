from enum import Enum

# storage type
class StorageType(Enum):
    NONE      = 0
    REG       = 1
    REG_ARR   = 2
    MEM       = 3

class TableHeader(Enum):
    BASEADDRESS   = 0
    TYPE          = 1
    OFFSETADDRESS = 2
    REGNAME       = 3
    WIDTH         = 4
    BITS          = 5
    FIELDNAME     = 6
    ACCESS        = 7
    RESETVALUE    = 8
    DESCRIPTION   = 9

class ParserState(Enum):
    IDLE        = 0
    PARSE_BLOCK = 1
    PARSE_REG   = 2
    PARSE_MEM   = 3
    PARSE_FIELD = 4
    END         = 5