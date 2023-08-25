import argparse
import sys
import os
import re
from xlsparse.parser import XlsParser
from base.macro import *

def main():
    arg_parser = argparse.ArgumentParser(description='xls2ralf script')
    arg_parser.add_argument('-m', '--mode',
                            type=str, default="module",
                            help="script mode, module or system")
    arg_parser.add_argument('-f', '--file',
                            type=str, default='',
                            help="register execl file")
    arg_parser.add_argument('-d', '--dirc',
                            type=str, default='',
                            help="register execl dictionary")
    arg_parser.add_argument('-o', '--output',
                            type=str, default='.',
                            help="ralf file output path")

    args = arg_parser.parse_args()

    # parament check
    if args.mode == "module":
        if not args.file:
            print("[Error] in module mode, must support register execl file, please check!")
            sys.exit()
        elif not os.path.exists(args.file):
            print(f"[Error] {args.file} dosen't exist, please check!")
            sys.exit()
        elif not re.match(FILE_NAME_PATTERN, args.file):
            print("[Error] invalid file name, it must be like \"xxx_project_xxx_module_reg_spec.xls(.xlsx)\", please check!")
            sys.exit()
    elif args.mode == "system":
        if not args.dirc:
            print("[Error] in system mode, must support register execl dictionary, please check!")
            sys.exit()            
        elif not os.path.lexists(args.dirc):
            print(f"[Error] {args.dirc} dosen't exist, please check!")
            sys.exit()
        elif not len(os.listdir()):
            print(f"[Error] {args.dirc} is empty, please check!")
            sys.exit()
    else:
        print(f"[Error] Unrecognized mode \"{args.mode}\", please check!")
        sys.exit()

    if os.path.lexists(args.output):
        output_path = os.path.abspath(args.output)
    else:
        print(f"[Error] {args.output} dosen't exist, please check!")
        sys.exit()

    # start parse execel
    xls_parser = XlsParser()
    if args.mode == "module":
        xls_parser.parse_xls(args.mode, args.file)
    else:
        xls_parser.parse_xls(args.mode, args.dirc)
    ralf = xls_parser.get_ralf()

    projetc_name = xls_parser.get_project_name()
    module_name = xls_parser.get_module_name()
    ralf_name = f"{module_name}.ralf" if args.mode == "module" else f"{projetc_name}.ralf"

    for base_addr, ral_code in ralf.items():
        if len(ralf) > 1:
            base_addr = base_addr.replace("\'h", "0x")
            temp_name = ralf_name.replace(".ralf", f"_{base_addr}.ralf")
        else:
            temp_name = ralf_name
        with open(f"{output_path}\{temp_name}", "w") as f:
            f.write(ral_code)

    print(f"[Info] ralf file is already output to {os.path.abspath(output_path)}, please confirm.")

main()
