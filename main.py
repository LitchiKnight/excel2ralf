import argparse
import sys
import os
import re
from parse.parser import ExcelParser
from base.macro import *

def main():
    arg_parser = argparse.ArgumentParser(description='excel2ralf script')

    arg_parser.add_argument('-s', action='store_true', default=False,
                            help="generate ralf file in system level")
    arg_parser.add_argument('-f', '--file',
                            type=str, default='',
                            help="specify a register Excel file to be converted")
    arg_parser.add_argument('-d', '--dir',
                            type=str, default='',
                            help="specify a directory which contents register Excel files")
    arg_parser.add_argument('-o', '--output',
                            type=str, default='.',
                            help="the output path of the converted ralf file")

    args = arg_parser.parse_args()
    

    if args.s: # system level
        try:
            if not args.dir:
                raise Exception("[Error] in system mode, must support register excel directory, please check!")
            if not os.path.lexists(args.dir):
                raise Exception(f"[Error] {args.dir} dosen't exist, please check!")
            if not len(os.listdir()):
                raise Exception(f"[Error] {args.dir} is empty, please check!")
        except Exception as e:
            print(e)
            sys.exit()
    else: # module level
        try:
            if not args.file:
                raise Exception("[Error] in module mode, must support register excel file, please check!")
            if not os.path.exists(args.file):
                raise Exception(f"[Error] {args.file} dosen't exist, please check!")
        except Exception as e:
            print(e)
            sys.exit()

    if os.path.lexists(args.output):
        output_path = os.path.abspath(args.output)
    else:
        print(f"[Error] {args.output} dosen't exist, please check!")
        sys.exit()

    # start parse execel
    excel_parser = ExcelParser()
    ralf_name = ""
    if args.s:
        excel_parser.parse_multi_files(args.dir)
        excel_parser.gen_system_ralf()
        ralf_name = f"{DEFAULT_SYSTEM_NAME}.ralf"
    else:
        excel_parser.parse_single_file(args.file)
        excel_parser.gen_module_ralf()
        module_name = excel_parser.get_module_name()
        ralf_name = f"{module_name}.ralf"
    ralf = excel_parser.get_ralf()
    print("[Info] all register Excel files are converted done.")

    for base_addr, ral_code in ralf.items():
        if len(ralf) > 1:
            base_addr = base_addr.replace("\'h", "0x")
            temp_name = ralf_name.replace(".ralf", f"_{base_addr}.ralf")
        else:
            temp_name = ralf_name
        with open(f"{output_path}\{temp_name}", "w") as f:
            f.write(ral_code)

    print(f"[Info] ralf file output directory: {os.path.abspath(output_path)}")

main()
