import argparse
import sys
import os
sys.path.append(r'..\xls2ralf')
import re
from xlsparse.parser import XlsParser
from base.macro import *

def main():
    arg_parser = argparse.ArgumentParser(description='xls2ralf script')
    arg_parser.add_argument('-f', '--file', type=str,
                            default='', required=True,
                            help="name of the excel file to be converted")
    arg_parser.add_argument('-o', '--output',
                            type=str, default='.',
                            help="location of the ralf file")

    args = arg_parser.parse_args()
    if os.path.exists(args.file):
        full_path = os.path.abspath(args.file)
        dir_path  = os.path.dirname(full_path)
        file_name = os.path.basename(full_path)
        os.chdir(dir_path)
    else:
        print(f"[Error] input file {args.file} dosen't exist, please check!")
        sys.exit()

    if os.path.lexists(args.output):
        output_path = os.path.abspath(args.output)
    else:
        print(f"[Error] output path {args.output} dosen't exist, please check!")
        sys.exit()

    xls_parser = XlsParser()
    xls_parser.parse_xls(file_name)
    ral = xls_parser.get_ral()

    if re.match(FILE_NAME_PATTERN, file_name):
        module_name = file_name.split("_")[2]
        ralf_name = f"{module_name}.ralf"
    else:
        ralf_name = f"{DEFAULT_BLOCK_NAME}.ralf"
    with open(f"{output_path}\{ralf_name}", "w") as f:
        f.write(ral)
    print(f"[Info] {ralf_name} is already output to {os.path.abspath(output_path)}, please confirm.")

main()
