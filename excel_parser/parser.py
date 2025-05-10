from typing import Any, List, Pattern
from common.base import Base
from common.const import TableHeader, AccessOptions, VALID_WIDTH, BASEADDR_PATTERN, TYPE_PATTERN, OFFSET_PATTERN, NAME_PATTERN, REGARR_WIDTH_PATTERN, WIDTH_PATTERN, BITS_PATTERN, ACCESS_PATTERN, RESET_PATTERN, HDL_PATTERN
from ral_model.ral_block import RalBlock
from ral_model.ral_register import RalRegister
from ral_model.ral_field import RalField

class ExcelParser:
    def __init__(self) -> None:
        self.table = None
        self.module = None

    def parse_table_cell(self, row: int, col: int, pattern: Pattern) -> str:
        """Parse the value of a table cell and validate it against a pattern."""
        if self.table is None:
            Base.error("Table is not initialized.")
        cell = self.table.cell_value(row, col)
        cell_pos = f'{chr(ord("A") + col)}{row + 1}'
        if isinstance(cell, float):
            cell = int(cell)
        value = str(cell).strip()
        if not pattern.match(value):
            Base.error(f'Invalid table cell value "{value}" at Excel [red]{cell_pos}[/red], please check!')
        return value

    def is_empty_cells(self, row: int, _range: range) -> bool:
        """Check if the cells in the specified range are empty."""
        return all(self.table.cell_type(row, col) == 0 for col in _range)
    
    def is_empty_block_cols(self, row: int) -> bool:
        """Check if the block columns are empty."""
        return self.is_empty_cells(row, range(TableHeader.BASEADDRESS.value, TableHeader.BASEADDRESS.value + 1))
    
    def is_empty_item_cols(self, row: int) -> bool:
        """Check if the item columns are empty."""
        return self.is_empty_cells(row, range(TableHeader.TYPE.value, TableHeader.REGRESETVALUE.value + 1))
    
    def is_empty_field_cols(self, row: int) -> bool:
        """Check if the field columns are empty."""
        return self.is_empty_cells(row, range(TableHeader.BITS.value, TableHeader.HDLPATH.value + 1))
    
    def is_table_end(self, row: int) -> bool:
        """Check if the table has ended."""
        return self.is_empty_cells(row, range(TableHeader.BASEADDRESS.value, TableHeader.FIELDRESETVALUE.value + 1))

    def get_bits_range(self, bits: str) -> int:
        """Get the range of bits from the bit string."""
        symbols = ["[", "]", " "]
        for s in symbols:
            bits = bits.replace(s, '')
        bits_arr = bits.split(':')
        if len(bits_arr) == 2:
            return int(bits_arr[0]) - int(bits_arr[1]) + 1
        elif len(bits_arr) == 1:
            return 1
        else:
            Base.error(f"Invalid bits format: {bits}")
            return -1
    
    def format_addr(self, addr: str) -> str:
        """Format the address string."""
        addr = addr.replace("0x", "\'h")  # 0x -> 'h
        addr = addr.replace("0X", "\'h")  # 0X -> 'h
        return addr

    def parse_block_col(self, row: int) -> RalBlock:
        """Parse the block column."""
        if self.module is None:
            Base.error("Module is not initialized.")
        block = RalBlock(self.module)
        block.baseaddr = self.format_addr(self.parse_table_cell(row, TableHeader.BASEADDRESS.value, BASEADDR_PATTERN))
        return block

    def parse_register_col(self, row: int) -> RalRegister:
        """Parse the register column."""
        register = RalRegister(self.parse_table_cell(row, TableHeader.REGNAME.value, NAME_PATTERN))
        register.offset = self.format_addr(self.parse_table_cell(row, TableHeader.OFFSETADDRESS.value, OFFSET_PATTERN))
        register.width  = self.parse_table_cell(row, TableHeader.WIDTH.value, WIDTH_PATTERN)
        register.reset  = self.parse_table_cell(row, TableHeader.REGRESETVALUE.value, RESET_PATTERN)
        return register

    def parse_field_col(self, row: int) -> RalField:
        """Parse the field column."""
        field = RalField(self.parse_table_cell(row, TableHeader.FIELDNAME.value, NAME_PATTERN))
        
        bits = self.parse_table_cell(row, TableHeader.BITS.value, BITS_PATTERN)
        cell_pos = f'{chr(ord("A") + TableHeader.BITS.value)}{row + 1}'
        bits_range = self.get_bits_range(bits)
        if bits_range > 0:
            field.bits = bits_range
        else:
            Base.error(f"Invalid table cell value '{bits}' at Excel [red]{cell_pos}[/red], please check!")
        
        access = self.parse_table_cell(row, TableHeader.ACCESS.value, ACCESS_PATTERN)
        cell_pos = f'{chr(ord("A") + TableHeader.ACCESS.value)}{row + 1}'
        if access.lower() in [option.value for option in AccessOptions]:
            field.access = access.lower()
        else:
            Base.error(f"Invalid table cell value '{access}' at Excel [red]{cell_pos}[/red], please check!")

        if not field.reserved:
            field.reset = self.parse_table_cell(row, TableHeader.FIELDRESETVALUE.value, RESET_PATTERN)
            if not self.is_empty_cells(row, range(TableHeader.HDLPATH.value, TableHeader.HDLPATH.value + 1)):
                field.hdl = self.parse_table_cell(row, TableHeader.HDLPATH.value, HDL_PATTERN)

        return field

    def init(self, excel: Any) -> None:
        """Initialize the parser with the Excel file."""
        self.table  = excel.sheets()[1]
        self.module = excel.sheet_names()[1]

    def parse_table(self) -> RalBlock:
        """Parse the entire table and return the top-level block."""
        table = self.table
        block = None

        for row in range(1, table.nrows):
            if self.is_table_end(row):
                break

            if not self.is_empty_block_cols(row):
                block = self.parse_block_col(row)

            if not self.is_empty_item_cols(row):
                if block is None:
                    Base.error("Block is not initialized.")
                block.add_register(self.parse_register_col(row))

            if not self.is_empty_field_cols(row):
                if block is None:
                    Base.error("Block is not initialized.")
                register = block.get_latest_register()
                register.add_field(self.parse_field_col(row))

        for rg in block.registers:
            rg.verify_fields()

        return block

    def run(self, excel: Any) -> RalBlock:
        """Run the parser on the given Excel file."""
        self.init(excel)
        return self.parse_table()
