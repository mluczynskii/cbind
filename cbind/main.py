import argparse 
import json
import wrappers

BOILERPLATE = "../cbind/interface.c"

def define_register(functions):
  """Adds luaL_Reg initialization to the generated source file"""
  names = [f["Name"] for f in functions]
  entries = [f'{{"{name}", c_{name}}}' for name in names]
  entries.append("{NULL, NULL}")
  return f"const luaL_Reg functions[] = {{\n{",\n".join(entries)}\n}};"

def main():
  parser = argparse.ArgumentParser(description="Generate .c source files")
  parser.add_argument("file", type=argparse.FileType("r"), nargs="+", help=".json files generated with parser.py")
  parser.add_argument("-o", "--output", type=argparse.FileType("w"), help="output .c file")
  args = parser.parse_args()
  output = args.output
  xs = []
  for file in args.file:
    ast = json.load(file)
    for function in ast:
      xs.append(wrappers.create_wrapper(function))
  with open(BOILERPLATE, "r") as boilerplate:
    for line in boilerplate:
      output.write(line)
  for wrapper in xs:
    body = "\n".join(wrapper["Body"])
    output.write(f"{wrapper["Signature"]} {{\n{body}\n}}")
  output.write(define_register(ast))

if __name__ == "__main__":
  main()