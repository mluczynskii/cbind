import argparse
import re
import json

def traverse(chunk, node, *path):
  """Move through the chunk along the path, starting from node"""
  if not path:
    raise ValueError("traverse: Path must be non-empty")
  for fieldname in path:
      index = node[fieldname]
      (s, node) = chunk[index]
  return (s, node)

def find_node(chunk, name):
  """Find FIRST node in a chunk with a given name"""
  nodes = find_nodes(chunk, name)
  if not nodes:
    raise ValueError(f"find_node: Node named {name} not found")
  return nodes[0]

def find_nodes(chunk, name):
  """Find EVERY node in a chunk with a given name"""
  return [traits for (s, traits) in chunk if s == name]

def function_name(chunk):
  """Get information about the function name"""
  root = find_node(chunk, "function_decl")
  (_, id_node) = traverse(chunk, root, "name")
  return id_node["strg"]

def return_type(chunk):
  """Get information about the function return type"""
  decl_node = find_node(chunk, "function_decl")
  return extract_type(chunk, traverse(chunk, decl_node, "type", "retn"))

# TODO: review implementation
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

# TODO: fix typename for non-fptr types
def extract_type(chunk, type_node):
  """Gather information about the type described by type_node"""
  (kind, traits) = type_node
  result = {"Kind": kind, "Typedef": "unql" in traits, "Pointer": None}
  if kind == "pointer_type":
      result["Typename"] = ""
      result["Pointer"] = extract_ptr(chunk, traits)
      return result
  if kind == "integer_type":
      (_, size_node) = traverse(chunk, traits, "size")
      if size_node["int"] == "8":
          result["Kind"] = "character_type"
  path = ["name"] if kind == "record_type" and not result["Typedef"] else ["name", "name"]
  (_, type_decl) = traverse(chunk, traits, *path)
  result["Typename"] = type_decl["strg"]
  return result

def function_arguments(chunk):
  """Gather information about the function arguments"""
  def argument_types():
    decl_node = find_node(chunk, "function_decl")
    result = []
    (_, prm) = traverse(chunk, decl_node, "type", "prms")
    while "chan" in prm:
        result.append(extract_type(chunk, traverse(chunk, prm, "valu")))
        (_, prm) = traverse(chunk, prm, "chan")
    return result
  parm_nodes = find_nodes(chunk, "parm_decl")
  names = [{"Name": f"var{idx}"} for idx in range(1, len(parm_nodes) + 1)]
  types = argument_types()
  return [{**name, **type_} for name, type_ in zip(names, types, strict=True)]

def find_structs(chunk):
  """Get info about every struct used in a function"""
  def find_owner(field_decl):
    """For a given field declaration, get typename of the corresponding record"""
    (_, record) = traverse(chunk, field_decl, "scpe")
    index = field_decl["scpe"]
    typedef = not "name" in record
    if typedef:
        candidates = find_nodes(chunk, "record_type")
        for candidate in candidates:
            if not "unql" in candidate or candidate["unql"] != index:
                continue
            else:
                record = candidate
                break
    path = ["name", "name"] if typedef else ["name"]
    (_, id_node) = traverse(chunk, record, *path)
    return id_node["strg"], typedef
  
  def convert_structs(structs: dict[str, dict], typedefs: dict[str, bool]):
    """Modify the structure of the result of extract_structs"""
    result = []
    for typename, fields in structs.items():
      converted = {
        "Typename": typename, 
        "Fields": fields,
        "Typedef": typedefs[typename]
      }
      result.append(converted)
    return result
  
  fields = find_nodes(chunk, "field_decl")
  result, typedefs = {}, {}
  if not fields:
    return result
  for field in fields:
    owner, typedef = find_owner(field)
    name = traverse(chunk, field, "name")[1]["strg"]
    type_ = extract_type(chunk, traverse(chunk, field, "type"))
    info = {"Name": name, **type_}
    if owner not in result:
      result[owner] = [info]
    else:
      result[owner].append(info)
    typedefs[owner] = typedef 
  return convert_structs(result, typedefs)

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
    raise ValueError(f"mk_node: Could not process line '{line}'")

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
  parser = argparse.ArgumentParser(
    prog="parser.py",
    description="GCC AST parser converting .original files into a JSON representation"
  )
  parser.add_argument(
    "infile",
    type=argparse.FileType("r"),
    nargs="+",
    help="AST files generated using -fdump-tree-original-raw"
  )
  parser.add_argument(
    "-o", "--output",
    type=argparse.FileType("w"),
    help="Output .json file (defaults to dump.json)"
  )
  args = parser.parse_args()
  outfile = args.output or open("dump.json", "w")
  for file in args.infile:
    lines = [" ".join(line.split()) for line in file if not re.match(r"^\s+$", line)]
    lines = coalesce(lines)
    output = {"Functions": [], "Structs": []}
    for chunk in chunks(lines): # First pass: collect information about API functions
      name = function_name(chunk)
      ret_type = return_type(chunk)
      args = function_arguments(chunk)
      function = {
         "Name": name,
         "Returns": ret_type,
         "Arguments": args 
      }
      output["Functions"].append(function)
    for chunk in chunks(lines): # Second pass: collect information about structs
      structs = find_structs(chunk)
      if not structs:
        continue
      output["Structs"] = output["Structs"] + structs
  outfile.write(json.dumps(output, indent=2))
  outfile.close()

if __name__ == "__main__":
  main()
