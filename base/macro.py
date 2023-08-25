# field access options
ACCESS_OPTIONS = [
    "rw", "ro", "wo", "w1", "w1c", "rc", "rs", "wrc",
    "wrs", "wc", "ws", "wsrc", "wcrs", "w1s", "w1t",
    "w0c", "w0s", "w0t", "w1src", "w1crs", "w0src",
    "w0crs", "woc", "wos", "wo1"
]

# register width options
VALID_WIDTH = [8, 16, 32]

# patterns
FILE_NAME_PATTERN    = "^[a-zA-Z0-9]+_project_[a-zA-Z0-9]+_module_reg_spec.xls(x?)$"
BASE_ADDR_PATTERN    = "^(0x|0X)[a-fA-F0-9]{8}$"
TYPE_PATTERN         = "^reg$|^mem$"
OFFSET_PATTERN       = "^(0x|0X)[a-fA-F0-9]{1,8}$"
NAME_PATTERN         = "^[a-zA-Z0-9_]+$"
REGARR_WIDTH_PATTERN = "^[1-9]+[0-9]*\*[1-9]+[0-9]*$"
WIDTH_PATTERN        = "^[1-9]+[0-9]*$|^[1-9]+[0-9]*\*[1-9]+[0-9]*[k,M,G]?$"
BITS_PATTERN         = "^\[[0-9]+(:([0-9]+))?\]$"
ACCESS_PATTERN       = "^[a-zA-Z0-9]+$"
RESET_PATTERN        = "(^[1-9]+[0-9]*\'b[0-1]+$)|(^[1-9]+[0-9]*\'h[a-fA-F0-9]+$)"

# default value
DEFAULT_BYTES = 4
DEFAULT_WIDTH = 32