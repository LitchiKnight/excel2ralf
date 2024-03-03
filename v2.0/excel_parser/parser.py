from common.base import Base
from common.const import *
from ral_model.ral_system import RalBlock

class ExcelParser:
  def __init__(self) -> None:
    pass

  # empty check
  def is_empty_cells(self, row, _range):
    return all(self.table.cell_type(row, col) == 0 for col in _range)
  
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
    return addr

  def parse_type(self, row):
    _type = self.table.cell_value(row, TYPE)
    return _type

  def parse_offset(self, row):
    offset = self.table.cell_value(row, OFFSETADDRESS)
    return offset

  def parse_regname(self, row):
    regname = self.table.cell_value(row, REGNAME)
    return regname

  def parse_width(self, row):
    width = self.table.cell_value(row, WIDTH)
    return width

  def parse_bits(self, row):
    bits = self.table.cell_value(row, BITS)
    bits = str(bits).strip()
    return bits[1]-bits[0]+1

  def parse_fieldname(self, row):
    filedname = self.table.cell_value(row, FIELDNAME)
    return filedname

  def parse_access(self, row):
    access = self.table.cell_value(row, ACCESS)
    return access

  def parse_resetvalue(self, row):
    resetvalue = self.table.cell_value(row, RESETVALUE)
    return resetvalue

  def parse_description(self, row):
    description = self.table.cell_value(row, DESCRIPTION)
    return description

  def add_block(self, row, ral):
    self.ral.baseaddr = self.parse_baseaddr(row)

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
