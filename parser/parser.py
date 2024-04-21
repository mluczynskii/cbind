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
parser.add_argument("filename")
args = parser.parse_args()

file_name = args.filename
res = None
try:

    file = open(file_name, "r")
    if(not validate_file(file)):
        raise Exception()
        #print("Invalid input file")

    res = json.dumps(run_parser(file))
    if args.verbose:
        print(res)
    file.close()

except FileNotFoundError:
    print("Could not open:", file_name)
    exit()
except:
    print("Invalid input file")
    exit()

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
