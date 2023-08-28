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
    arg_parser.add_argument('-d', '--dirc',
                            type=str, default='',
                            help="specify a directory which contents register Excel files")
    arg_parser.add_argument('-o', '--output',
                            type=str, default='.',
                            help="the output path of the converted ralf file")

    args = arg_parser.parse_args()
    

    if args.s: # system level
        try:
            if not args.dirc:
                raise Exception("[Error] in system mode, must support register execl dictionary, please check!")
            elif not os.path.lexists(args.dirc):
                raise Exception(f"[Error] {args.dirc} dosen't exist, please check!")
            elif not len(os.listdir()):
                raise Exception(f"[Error] {args.dirc} is empty, please check!")
        except Exception as e:
            print(e)
            sys.exit()
    else: # module level
        try:
            if not args.file:
                raise Exception("[Error] in module mode, must support register execl file, please check!")
            elif not os.path.exists(args.file):
                raise Exception(f"[Error] {args.file} dosen't exist, please check!")
            elif not re.match(FILE_NAME_PATTERN, args.file):
                raise Exception("[Error] invalid file name, it must be like \"xxx_project_xxx_module_reg_spec.xls(.xlsx)\", please check!")
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
    if args.s:
        excel_parser.parse_multi_files(args.dirc)
    else:
        excel_parser.parse_single_file(args.file)
    ralf = excel_parser.get_ralf()

    projetc_name = excel_parser.get_project_name()
    module_name = excel_parser.get_module_name()
    ralf_name = f"{projetc_name}.ralf" if args.s else f"{module_name}.ralf"

    for base_addr, ral_code in ralf.items():
        if len(ralf) > 1:
            base_addr = base_addr.replace("\'h", "0x")
            temp_name = ralf_name.replace(".ralf", f"_{base_addr}.ralf")
        else:
            temp_name = ralf_name
        with open(f"{output_path}\{temp_name}", "w") as f:
            f.write(ral_code)

    print(f"[Info] ralf file already output to {os.path.abspath(output_path)}, please confirm.")

main()
