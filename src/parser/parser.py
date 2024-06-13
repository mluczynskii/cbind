import argparse
import json
from parse_functions import *

parser = argparse.ArgumentParser(
    prog="parser",
    description="Parser of intermediate language tree."
    )

parser.add_argument("-o", "--output", help="name of the output file")
parser.add_argument("-v", "--verbose", action="store_true", help="output result into terminal")
parser.add_argument("--no-dump", action="store_true", help="do not produce output file")
parser.add_argument("filename", nargs="+", help="list of input files")
parser.add_argument("-f", "--functions", help="file containing names of functions to include")
args = parser.parse_args()

file_names = args.filename

res = []
functions = []

if args.functions != None:
    try: 
        f = open(args.functions, "r")
        functions = [fun.strip() for fun in  f.readlines()]

    except FileNotFoundError:
        print("Could not open:", file_names)
        exit()

for file in file_names:
    try:

        f = open(file, "r")
        if(not validate_file(f)):
            raise Exception("Invalid input file")
        res += run_parser(f, functions)
        f.close()

    except FileNotFoundError:
        print("Could not open:", file_names)
        exit()

res = json.dumps(res, indent=2)

if args.verbose:
    print(res)

if not args.no_dump:
    try:
        file_name = "data.json"
        if args.output != None:
            file_name = args.output
        file = open(file_name, "w")

        file.write(res)
        file.write("\n")
        file.close()
    except:
        print("Could not produce output file")
