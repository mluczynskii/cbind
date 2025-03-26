import argparse
import re  
from json import dumps

def traverse(chunk, start, *path): 
  """Move through the node chunk along the path"""
  node = start 
  for fieldname in path: 
    (s, node) = chunk[node[fieldname]]
  return (s, node)

def find_node(chunk, name): 
  """Return FIRST node in a chunk with a given name"""
  return find_nodes(chunk, name)[0]

def find_nodes(chunk, name): 
  """Return EVERY node in a chunk with a given name"""
  result = [traits for (s, traits) in chunk if s == name]
  if not result:
    raise Exception(f"No nodes named {name} found.")
  return result 
  
def function_name(chunk): 
  root = find_node(chunk, "function_decl")
  (_, id_node) = traverse(chunk, root, "name")
  return {"Name": id_node["strg"]}

def extract_ptr(chunk, type_node):
  """Extracts information about a pointer"""
  (kind, type_decl) = traverse(chunk, type_node, "ptd")
  if kind == "function_type":
    data = {"Arguments": []}
    data["Returns"] = extract_type(chunk, *traverse(chunk, type_decl, "retn"))
    (_, prm) = traverse(chunk, type_decl, "prms")
    while "chan" in prm:
      data["Arguments"].append(extract_type(chunk, *traverse(chunk, prm, "valu")))
      (_, prm) = traverse(chunk, prm, "chan")
  else:
    data = extract_type(chunk, kind, type_decl)
  return data

def extract_type(chunk, kind, type_node):
  """Gather information about the type described by type_node"""
  result = {"Kind": kind, "Typedef": "unql" in type_node}
  if kind == "integer_type":
    (_, sz_node) = traverse(chunk, type_node, "size")
    if sz_node["int"] == "8":
      result["Kind"] = "character_type"
  if kind == "pointer_type":
    result["Pointer"] = extract_ptr(chunk, type_node)
    return result
  if kind == "record_type" and not result["Typedef"]:
    (_, type_decl) = traverse(chunk, type_node, "name")
  else:
    (_, type_decl) = traverse(chunk, type_node, "name", "name")
  result["Typename"] = type_decl["strg"]
  return result

def return_type(chunk): 
  """Return information about the function return type"""
  root = find_node(chunk, "function_decl")
  (kind, type_node) = traverse(chunk, root, "type", "retn")
  return extract_type(chunk, kind, type_node)

def argument_names(chunk):
  """Generate variable names for the function arguments"""
  argcount = len(find_nodes(chunk, "parm_decl")) 
  return [{"Name": f"var{idx}"} for idx in range(1, argcount+1)]

def argument_types(chunk): 
  """Iterate over tree_nodes to get function argument types in correct order"""
  result = []
  (_, prm) = traverse(chunk, find_node(chunk, "function_decl"), "type", "prms") 
  while "chan" in prm:
    result.append(extract_type(chunk, *traverse(chunk, prm, "valu")))
    (_, prm) = traverse(chunk, prm, "chan")
  return result

def function_arguments(chunk): 
  """Combine argument_names with argument_types"""
  names = argument_names(chunk)
  types = argument_types(chunk) 
  return [{**name, **type_} for name, type_ in zip(names, types, strict=True)]

def mk_node(line): 
  """Convert a single AST line into a pair (node_name, node_parameters)"""
  if match := re.fullmatch(r"^@\d+ (?P<name>\w+) (?P<params>.*)$", line):
    traits = {}
    for arg, val in re.findall(r"([a-z]+) ?: ([^\s]+)", match.group("params")):
      if match_val := re.match(r"@(?P<id>\d+)", val):
        traits[arg] = int(match_val.group("id")) - 1
      else:
        traits[arg] = val
    return (match.group("name"), traits)
  else:
    raise Exception(f"mk_node: could not process line '{line}'")

def chunks(lines): 
  """Splits the whole AST file into per-function chunks"""
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
  """Adjusts the AST so that every node description takes up one line"""
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
    for chunk in chunks(lines):
      result = {**function_name(chunk), "Returns": return_type(chunk)}
      result["Arguments"] = function_arguments(chunk)
      functions.append(result)
  with open("dump.json", "w") as output:
    output.write(dumps(functions, indent=2))

if __name__ == "__main__":
  main()