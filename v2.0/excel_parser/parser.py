from common.base import Base
from common.const import *

class ExcelParser:
  def __init__(self) -> None:
    pass

  # empty check
  def is_empty_cells(self, row, _range):
    return all(self.table.cell_type(row, col) is 0 for col in _range)
  
  def is_block_empty(self, row):
    return self.is_empty_cells(row, range(BASEADDRESS, BASEADDRESS+1))
  
  def is_item_empty(self, row):
    return self.is_empty_cells(row, range(TYPE, WIDTH+1))
  
  def is_field_empty(self, row):
    return self.is_empty_cells(row, range(BITS, DESCRIPTION+1))
  
  def is_table_end(self, row):
    return self.is_empty_cells(row, range(BASEADDRESS, DESCRIPTION+1))
  
  # parse table cell
  def parse_baseaddr(self, row):
    addr = self.table.cell_value(row, BASEADDRESS)
    Base.print(addr)

  def parse_type(self, row):
    _type = self.table.cell_value(row, TYPE)
    Base.print(_type)

  def parse_offset(self, row):
    pass

  def parse_regname(self, row):
    pass

  def parse_width(self, row):
    pass

  def parse_bits(self, row):
    pass

  def parse_fieldname(self, row):
    pass

  def parse_access(self, row):
    pass

  def parse_resetvalue(self, row):
    pass

  def parse_description(self, row):
    pass

  def add_block(self, row, ral):
    self.parse_baseaddr(row)

  def add_register(self, row, ral):
    self.parse_type(row)
    self.parse_offset(row)
    self.parse_regname(row)
    self.parse_width(row)

  def add_field(self, row, ral):
    self.parse_bits(row)
    self.parse_fieldname(row)
    self.parse_access(row)
    self.parse_resetvalue(row)
    self.parse_description(row)

  # main process

  def init(self, excel):
    self.table = excel.sheets()[1]
    self.module = excel.sheet_names()[1]
    #TODO: create ral model instance

  def parse_table(self):
    table = self.table

    for row in range(table.nrows):
      if self.is_table_end(row):
        break

      if not self.is_block_empty(row):
        Base.print(f"create block {self.module}")
        self.add_block(row, None)

      if not self.is_item_empty(row):
        Base.print(f"  create register {table.cell_value(row, REGNAME)}")
        self.add_register(row, None)

      if not self.is_field_empty(row):
        Base.print(f"    create field {table.cell_value(row, FIELDNAME)}")
        self.add_field(row, None)

  def run(self, excel):
    self.init(excel)
    self.parse_table()
