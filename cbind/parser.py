import argparse
import re  
from json import dumps

def traverse(chunk, start, *path): 
  node = start 
  for fieldname in path: 
    (s, node) = chunk[node[fieldname]]
  return (s, node)

def find_node(chunk, name): 
  return find_nodes(chunk, name)[0]

def find_nodes(chunk, name): 
  result = [traits for (s, traits) in chunk if s == name]
  if not result:
    raise Exception(f"No nodes named {name} found.")
  return result 
  
def function_name(chunk): 
  decl_node = find_node(chunk, "function_decl")
  (_, id_node) = traverse(chunk, decl_node, "name")
  return {"Name": id_node["strg"]}

def extract_type(chunk, kind, type_node):
  result = {"Kind": kind}
  if kind == "integer_type":
    (_, sz_node) = traverse(chunk, type_node, "size")
    if sz_node["int"] == "8":
      result["Kind"] = "character_type"
  result["Typedef"] = "unql" in type_node
  format = []
  if kind == "record_type" and not result["Typedef"]:
    (_, type_decl) = traverse(chunk, type_node, "name")
    format.append("struct")
  elif kind == "pointer_type":
    return {}
  else:
    (_, type_decl) = traverse(chunk, type_node, "name", "name")
  result["Typename"] = type_decl["strg"]
  format.append(result["Typename"])
  result["Format"] = " ".join(format + ["{name}"])
  return result

def return_type(chunk): 
  decl_node = find_node(chunk, "function_decl")
  (kind, type_node) = traverse(chunk, decl_node, "type", "retn")
  return extract_type(chunk, kind, type_node)

def argument_names(chunk): 
  result = []
  for node in find_nodes(chunk, "parm_decl"):
    (_, id_node) = traverse(chunk, node, "name")
    result.append({"Name": id_node["strg"]})
  return result

def argument_types(chunk):   
  result = []
  for node in find_nodes(chunk, "parm_decl"):
    (kind, type_node) = traverse(chunk, node, "type")
    result.append(extract_type(chunk, kind, type_node))
  return result

def function_arguments(chunk): 
  names = argument_names(chunk)
  types = argument_types(chunk) 
  return [{**name, **type_} for name, type_ in zip(names, types, strict=True)]

def mk_node(line): 
  if match := re.fullmatch(r"^@\d+ (?P<name>\w+) (?P<params>.*)$", line):
    traits = {}
    for arg, val in re.findall(r"([a-z]+): ([^\s]+)", match.group("params")):
      if match_val := re.match(r"@(?P<id>\d+)", val):
        traits[arg] = int(match_val.group("id")) - 1
      else:
        traits[arg] = val
    return (match.group("name"), traits)
  else:
    raise Exception(f"mk_node: could not process line '{line}'")

def chunks(lines): 
  chunk = []
  for line in lines[2:]:
    if re.fullmatch(r"^;;.*$", line):
      if re.fullmatch(r"^;; Function.*$", line):
        yield chunk
      chunk = []
    else:
      node = mk_node(line)
      chunk.append(node) 
  yield chunk

def coalesce(lines): 
  result, acc = [], ""
  for line in lines:
    if re.match(r"^(?:@)|(?:;;).+$", line):
      if acc:
        result.append(acc)
      acc = line 
    else:
      acc = f"{acc} {line}"
  result.append(acc)
  return result

def main():
  parser = argparse.ArgumentParser(description="GCC AST parser")
  parser.add_argument("file", type=argparse.FileType("r"), nargs="+", help=".original AST files generated using -fdump-tree-original-raw")
  parser.add_argument("-f", "--filter", help="text file containing desired function names")
  args = parser.parse_args()
  functions = []
  for file in args.file:
    lines = [" ".join(line.split()) for line in file if not re.match(r"^\s+$", line)]
    lines = coalesce(lines)
    for chunk in chunks(lines): # TODO:
      result = {**function_name(chunk), **return_type(chunk)}
      result["Arguments"] = function_arguments(chunk)
      functions.append(result)
  with open("dump.json", "w") as output:
    output.write(dumps(functions, indent=2))

if __name__ == "__main__":
  main()