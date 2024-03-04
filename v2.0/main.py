import os
import xlrd
import argparse
from common.base import Base
from excel_parser.parser import ExcelParser

def check_arg(args):
  file       = args.file
  output     = args.output
  abs_output = os.path.abspath(output)

  # check file exists or not
  if file:
    exts = {'.xls', '.xlsx'}
    if not os.path.exists(file):
      Base.error(f"[bold]{file}[/bold] is not exists, please check!")
    elif not os.path.splitext(file)[1] in exts:
      Base.error(f"[bold]{file}[/bold] is not an Excel file, please check!")
  else:
    Base.error("you must specify an Excel file, please check!")

  # check output path exists or not
  if not os.path.exists(abs_output):
    Base.error(f"{abs_output} is not exists, please check!")

def main():
  arg_parser = argparse.ArgumentParser(description='transform register Excel file to RALF file')
  arg_parser.add_argument('-f', '--file'  , type=str, default='' , help="specify a register Excel file")
  arg_parser.add_argument('-o', '--output', type=str, default='.', help="specify the output path of the ralf file")

  args = arg_parser.parse_args()
  check_arg(args)

  file_name = os.path.basename(args.file)
  Base.info(f"Start transform {file_name}")

  excel = Base.run_with_animation("Reading Excel file...", xlrd.open_workbook, args.file)
  parser = ExcelParser()

  Base.run_with_animation("Parsing Excel file...", parser.run, excel)
  with open(f'{parser.module}.ralf', 'w') as f:
    Base.run_with_animation("Generating RALF file...", f.write, parser.get_ralf_code())
  Base.info(f"output {parser.module}.ralf")

if __name__ == "__main__":
  main()