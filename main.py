import argparse
import sys
import os
sys.path.append(r'..\xls2ralf')
from xls.parser import Parser
from base.default import *

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
        file_path = args.file
        file_name = os.path.basename(file_path)
        project_name = file_name.split("_")[0]
        module_name = file_name.split("_")[2]
    else:
        print(f"[Error] input file {args.file} dosen't exist, please check!")
        sys.exit()

    if os.path.lexists(args.output):
        output_path = os.path.abspath(args.output)
    else:
        print(f"[Error] output path {args.output} dosen't exist, please check!")
        sys.exit()

    xls_parser = Parser()
    if module_name:
        xls_parser.set_module_name(module_name)
    xls_parser.xls2ralf(file_path)
    ral = xls_parser.get_ral()

    ralf_name = f"{module_name if module_name else BLOCK_NAME}.ralf"
    with open(f"{output_path}\{ralf_name}", "w") as f:
        f.write(ral)
    print(f"[Info] {ralf_name} is already output to {os.path.abspath(output_path)}, please check.")

main()
