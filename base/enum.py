from enum import Enum

# storage type
class StorageType(Enum):
    REG       = 1
    REG_ARRAY = 2
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
    PARSE_REG   = 1
    PARSE_MEM   = 2
    PARSE_FIELD = 3
    END         = 4