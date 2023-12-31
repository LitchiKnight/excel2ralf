import argparse
import sys
import os
import re
from parse.parser import ExcelParser
from base.macro import *

def main():
    arg_parser = argparse.ArgumentParser(description='transform register Excel file to RALF file')

    arg_parser.add_argument('-s', action='store_true', default=False,
                            help="generate ralf file in system level")
    arg_parser.add_argument('-f', '--file',
                            type=str, default='',
                            help="specify a register Excel file to be transformed")
    arg_parser.add_argument('-d', '--directory',
                            type=str, default='',
                            help="specify a directory which contents register Excel files")
    arg_parser.add_argument('-o', '--output',
                            type=str, default='.',
                            help="specify the output path of the tansformed ralf file")

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
        file_list = os.listdir(args.dir)
        for file in file_list:
             excel_parser.parse_excel_file(os.path.join(args.dir, file))
        excel_parser.gen_system_ralf()
        ralf_name = f"{DEFAULT_SYSTEM_NAME}.ralf"
    else:
        excel_parser.parse_excel_file(args.file)
        excel_parser.gen_module_ralf()
        module_name = excel_parser.get_module_name()
        ralf_name = f"{module_name}.ralf"
    ralf = excel_parser.get_ralf()
    print("[Info] all register Excel files are transformed done.")

    for base_addr, ral_code in ralf.items():
        abs_file_path = os.path.join(output_path, ralf_name)
        if len(ralf) > 1:
            base_addr = base_addr.replace("\'h", "0x")
            abs_file_path = os.path.join(output_path, ralf_name.replace(".ralf", f"_{base_addr}.ralf"))
        with open(abs_file_path, "w") as f:
            f.write(ral_code)

    print(f"[Info] ralf file output directory: {output_path}")

# execute main function
main()
