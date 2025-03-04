import argparse 
import json
import util

HEADERS = ["lua.h", "lualib.h", "callback.h", "stdlib.h"]
BOILERPLATE = "interface.json"

def add_headers(output):
  for header in HEADERS:
    output.write(f"#include <{header}>\n")

def add_interface(output):
  pass

def main():
  parser = argparse.ArgumentParser(description="Generate .c source files")
  parser.add_argument("file", type=argparse.FileType("r"), nargs="+", help=".json files generated with parser.py")
  args = parser.parse_args()
  for file in args.file:
    ast = json.load(file)

if __name__ == "__main__":
  main()