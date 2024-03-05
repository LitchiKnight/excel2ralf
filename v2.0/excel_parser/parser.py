import re
from common.base import Base
from common.const import *
from ral_model.ral_block import RalBlock
from ral_model.ral_register import RalRegister
from ral_model.ral_field import RalField

class ExcelParser:
  def __init__(self) -> None:
    pass

  # empty check
  def is_empty_cells(self, row: int, _range: range) -> bool:
    return all(self.table.cell_type(row, col) == 0 for col in _range)
  
  def is_empty_block_cols(self, row: int) -> bool:
    return self.is_empty_cells(row, range(BASEADDRESS, BASEADDRESS+1))
  
  def is_empty_item_cols(self, row: int) -> bool:
    return self.is_empty_cells(row, range(TYPE, REGRESETVALUE+1))
  
  def is_empty_field_cols(self, row: int) -> bool:
    return self.is_empty_cells(row, range(BITS, FIELDRESETVALUE+1))
  
  def is_table_end(self, row: int) -> bool:
    return self.is_empty_cells(row, range(BASEADDRESS, FIELDRESETVALUE+1))

  # format functions
  def get_bits_range(self, bits: str) -> int:
    symbols = ["[", "]", " "]
    for s in symbols:
      bits = bits.replace(s, '')
    bits_arr = bits.split(':')
    if len(bits_arr) == 2:
      return int(bits_arr[0])-int(bits_arr[1])+1
    elif len(bits_arr) == 1:
      return 1
    else:
      return -1
    
  def format_addr(self, addr: str) -> str:
    addr = addr.replace("0x", "\'h") # 0x -> 'h
    addr = addr.replace("0X", "\'h") # 0X -> 'h
    return addr

  # parse functions
  def parse_table_cell(self, row: int, col: int, pattern: str) -> str:
    cell = self.table.cell_value(row, col)
    cell_pos = f'{chr(ord("A")+col)}{row+1}'
    if type(cell) == float:
      cell = int(cell)
    value = str(cell).strip()
    if value:
      if not re.match(pattern, value):
        Base.error(f'invalid table cell value "{value}" at Excel [red]{cell_pos}[/red], please check!')
    else:
        Base.error(f'empty table cell at Excel [red]{cell_pos}[/red], please check!')
    return value

  def parse_block_col(self, row: int) -> RalBlock:
    block = RalBlock(self.module)
    block.baseaddr = self.format_addr(self.parse_table_cell(row, BASEADDRESS, BASEADDR_PATTERN))
    return block

  def parse_register_col(self, row: int) -> RalRegister:
    register = RalRegister(self.parse_table_cell(row, REGNAME, NAME_PATTERN))
    register.offset = self.format_addr(self.parse_table_cell(row, OFFSETADDRESS, OFFSET_PATTERN))
    register.width  = self.parse_table_cell(row, WIDTH, WIDTH_PATTERN)
    register.reset  = self.parse_table_cell(row, REGRESETVALUE, RESET_PATTERN)
    return register

  def parse_field_col(self, row: int) -> RalField:
    field = RalField(self.parse_table_cell(row, FIELDNAME, NAME_PATTERN))
    
    bits = self.parse_table_cell(row, BITS, BITS_PATTERN)
    cell_pos = f'{chr(ord("A")+BITS)}{row+1}'
    bits_range = self.get_bits_range(bits)
    if bits_range > 0:
      field.bits = bits_range
    else:
      Base.error(f'invalid table cell value "{bits}" at Excel [red]{cell_pos}[/red], please check!')
    
    access = self.parse_table_cell(row, ACCESS, ACCESS_PATTERN)
    cell_pos = f'{chr(ord("A")+ACCESS)}{row+1}'
    if access.lower() in ACCESS_OPTIONS:
      field.access = access.lower()
    else:
      Base.error(f'invalid table cell value "{access}" at Excel [red]{cell_pos}[/red], please check!')

    if not field.reserved:
      field.reset = self.parse_table_cell(row, FIELDRESETVALUE, RESET_PATTERN)

    return field

  # main process
  def init(self, excel: object) -> None:
    self.table  = excel.sheets()[1]
    self.module = excel.sheet_names()[1]

  def parse_table(self) -> RalBlock:
    table = self.table
    block = None

    for row in range(1, table.nrows):
      if self.is_table_end(row):
        break

      if not self.is_empty_block_cols(row):
        block = self.parse_block_col(row)

      if not self.is_empty_item_cols(row):
        block.add_register(self.parse_register_col(row))

      if not self.is_empty_field_cols(row):
        register = block.get_latest_register()
        register.add_field(self.parse_field_col(row))

    return block

  def run(self, excel: object) -> RalBlock:
    self.init(excel)
    return self.parse_table()

