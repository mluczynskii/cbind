import argparse
import re
import json

def traverse(chunk, node, *path):
  """
  Moves through the chunk along the path, starting from node.

  Args:
    chunk: A list of nodes relevant to the currently processed function.
    node: Starting node.
    *path: Names of the consecutive fields on the path.
  
  Raises:
    ValueError: Provided path is empty.

  Returns:
    (name, node): A pair consisting of the final node name and the node itself.
  """
  if not path:
    raise ValueError("traverse: Path must be non-empty")
  for fieldname in path:
      index = node[fieldname]
      (s, node) = chunk[index]
  return (s, node)

def find_node(chunk, name: str):
  """
  Find FIRST node in a chunk with a given name.

  Args:
    chunk: A list of nodes relevant to the currently processed function.
    name (str): Name of a requested node. 
  
  Raises:
    ValueError: A node of a given `name` is nowhere to be found.

  Returns:
    node: A node with a given `name`.
  """
  nodes = find_nodes(chunk, name)
  if not nodes:
    raise ValueError(f"find_node: Node named {name} not found")
  return nodes[0]

def find_nodes(chunk, name):
  """
  Find EVERY node in a chunk with a given name.

  Args:
    chunk: A list of nodes relevant to the currently processed function.
    name: Name of the requested nodes.
  
  Returns:
    nodes: A list of nodes with a given `name` (can be empty)
  """
  return [traits for (s, traits) in chunk if s == name]

def function_name(chunk):
  """
  Finds the name of the function described by a chunk.

  Args:
    chunk: A list of nodes relevant to the currently processed function.

  Returns:
    name: Name of the currently processed function. 
  """
  root = find_node(chunk, "function_decl")
  (_, id_node) = traverse(chunk, root, "name")
  return id_node["strg"]

def return_type(chunk):
  """
  Extracts function return type information in the provided chunk.

  Args:
    chunk: A list of nodes relevant to the currently processed function.
  
  Returns:
    info: A dictionary better described by the `extract_type` function.
  """
  decl_node = find_node(chunk, "function_decl")
  return extract_type(chunk, traverse(chunk, decl_node, "type", "retn"))

def extract_ptr(chunk, type_node):
  """
  Extracts information about a pointer.

  Args:
    chunk: A list of nodes relevant to the currently processed function.
    type_node: Root node for the type declaration (ex. *function_type*).

  Returns:
    (data, typename): A dictionary describing the underlying type (same as `extract_type`)
      and a full typename of the pointer.   
  """
  def fptr_typename(data):
    if "unql" in type_node: 
      (_, id_node) = traverse(chunk, type_node, "name", "name")
      return id_node["strg"]
    arglist = ",".join([
      arg["Typename"] for arg in data["Arguments"]
    ])
    returns = data["Returns"]["Typename"]
    return f"{returns} (*)({arglist})"
  
  (kind, type_decl) = traverse(chunk, type_node, "ptd")
  if kind == "function_type":
      data = {"Arguments": [], "Kind": kind}
      data["Returns"] = extract_type(chunk, traverse(chunk, type_decl, "retn"))
      (_, prm) = traverse(chunk, type_decl, "prms")
      while "chan" in prm:
          data["Arguments"].append(extract_type(chunk, traverse(chunk, prm, "valu")))
          (_, prm) = traverse(chunk, prm, "chan")
      typename = fptr_typename(data)
  else:
      data = extract_type(chunk, kind, type_decl)
      typename = f"{data["Typename"]}*"
  return data, typename

def extract_type(chunk, type_node):
  """
  Gather information about the type described by type_node.

  Args:
    chunk: A list of nodes relevant to the currently processed function.
    type_node: Root node for the type declaration (ex. *integer_type*).

  Returns:
    dict: A dictionary describing the type
        - Kind (str): The type family to which the type belongs (ex. void_type or character_type),
        - Typedef (bool): Whether the type is declared using a typedef (used in structs),
        - Pointer: Underlying type information (if the type is a pointer) or None,
        - Typename (str): The name of the type (ex. *int* or *pair_t*)
  """
  (kind, traits) = type_node
  result = {"Kind": kind, "Typedef": "unql" in traits, "Pointer": None}
  if kind == "pointer_type":
      result["Pointer"], result["Typename"] = extract_ptr(chunk, traits)
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
  """
  Gather information about the function arguments
  
  Args:
    chunk: A list of nodes relevant to the currently processed function.
  
  Returns:
    xs: A list of dictionaries dictated by the `extract_type` function.
  """
  decl_node = find_node(chunk, "function_decl")
  xs = []
  (_, prm) = traverse(chunk, decl_node, "type", "prms")
  while "chan" in prm:
      xs.append(extract_type(chunk, traverse(chunk, prm, "valu")))
      (_, prm) = traverse(chunk, prm, "chan")
  return xs

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
  """
  Converts a single AST line into a pair (node_name, node_parameters)
  
  Args:
    line: Single line corresponding to one full (!) node description.

  Raises:
    ValueError: Provided line does not match the format of the GCC AST node.

  Returns:
    (name, node): The name of the node and it's parameters
  """
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
  """
  Splits the whole AST file into per-function chunks.

  Args:
    lines: Every line of the AST dump as a list.

  Returns:
    chunks: List of lists of nodes making up specific chunks.
  """
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
  """
  Adjusts the AST so that every node description takes up one line.
  
  Args:
    lines: Every line of the AST dump as a list.
  """
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
