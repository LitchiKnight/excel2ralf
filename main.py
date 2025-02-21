import argparse
from pathlib import Path
import xlrd
from common.base import Base
from excel_parser.parser import ExcelParser

def check_arg(file: Path, output: Path) -> None:
    exts = {'.xls', '.xlsx'}
    
    if not file.exists():
        Base.error(f"[bold]{file}[/bold] does not exist, please check!")
    elif file.suffix not in exts:
        Base.error(f"[bold]{file}[/bold] is not an Excel file, please check!")
    
    if not output.exists():
        output.mkdir(parents=True, exist_ok=True)

def main() -> None:
    arg_parser = argparse.ArgumentParser(description='Transform register Excel file to RALF file')
    arg_parser.add_argument('-f', '--file', type=Path, required=True, help="Specify a register Excel file")
    arg_parser.add_argument('-o', '--output', type=Path, default=Path('.'), help="Specify the output path of the RALF file")

    args = arg_parser.parse_args()
    check_arg(args.file, args.output)

    file_name = args.file.name
    Base.info(f"Start transforming {file_name}")

    parser = ExcelParser()
    excel = Base.run_with_animation("Reading Excel file...", xlrd.open_workbook, str(args.file))
    model = Base.run_with_animation("Parsing Excel file...", parser.run, excel)
    module = parser.module

    output_file = args.output / f'{module}.ralf'
    with output_file.open('w') as f:
        Base.run_with_animation("Generating RALF file...", f.write, model.gen_ralf_code())
    Base.info(f"Output {output_file}")

if __name__ == "__main__":
    main()