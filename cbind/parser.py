import argparse
import re
import json

def traverse(chunk, node, *path):
  if not path:
    raise ValueError("traverse: Path must be non-empty")
  for fieldname in path:
      index = node[fieldname]
      node_type, node = chunk[index]
  return node_type, node

def find_node(chunk, name: str):
  nodes = find_nodes(chunk, name)
  if not nodes:
    raise ValueError(f"find_node: Node named {name} not found")
  return nodes[0]

def find_nodes(chunk, name):
  return [traits for (s, traits) in chunk if s == name]

def function_name(chunk):
  root = find_node(chunk, "function_decl")
  _, id_node = traverse(chunk, root, "name")
  return id_node["strg"]

def return_type(chunk):
  decl_node = find_node(chunk, "function_decl")
  return extract_type(chunk, *traverse(chunk, decl_node, "type", "retn"))

def extract_function_pointer(chunk, type_node):
  argument_data = []
  return_data = extract_type(chunk, *traverse(chunk, type_node, "retn"))
  _, prm = traverse(chunk, type_node, "prms")
  while "chan" in prm:
    argument_data.append(extract_type(chunk, *traverse(chunk, prm, "valu")))
    _, prm = traverse(chunk, prm, "chan")
  return return_data, argument_data

def pointer_typename(chunk, kind, type_node):
  assert(kind == "pointer_type")
  kind_2, type_node_2 = traverse(chunk, type_node, "ptd")
  if kind_2 != "function_type":
    type_data = extract_type(chunk, kind_2, type_node_2)
    return f'{type_data["typename"]}*'
  elif "unql" in type_node:
    _, identifier_node = traverse(chunk, type_node, "name", "name")
    return identifier_node["strg"]
  return_data, argument_data = extract_function_pointer(chunk, type_node_2)
  arguments = ",".join([data["typename"] for data in argument_data])
  return f'{return_data["typename"]} (*)({arguments})'

def extract_type(chunk, kind, type_node):
  typedef = "unql" in type_node
  if kind == "integer_type":
    _, size_node = traverse(chunk, type_node, "size")
    if size_node["int"] == "8":
      kind = "character_type"
  if kind == "function_type":
    return {"kind": kind, "typename": None}
  if kind != "pointer_type":
    path = ["name"] if kind in ["record_type", "union_type", "enumeral_type"] and not typedef else ["name", "name"]
    _, type_declaration = traverse(chunk, type_node, *path)
    typename = type_declaration["strg"]
    if not typedef and kind == "record_type":
      typename = f'struct {typename}'
    elif not typedef and kind == "union_type":
      typename = f'union {typename}'
    elif not typedef and kind == "enumeral_type":
      typename = f'enum {typename}'
  else:
    typename = pointer_typename(chunk, kind, type_node)
  return {"kind": kind, "typename": typename}

def extract_enums(chunks):

  def enum_name(chunk, enum_declaration):
    typedef = "unql" in enum_declaration
    path = ["name", "name"] if typedef else ["name"]
    _, identifier_node = traverse(chunk, enum_declaration, *path)
    name = identifier_node["strg"]
    return name if typedef else f"enum {name}" 

  def enum_fields(chunk, enum_declaration):
    fields = []
    _, prm = traverse(chunk, enum_declaration, "csts")
    while True:
      _, identifier_node = traverse(chunk, prm, "purp")
      _, integer_cst = traverse(chunk, prm, "valu", "cnst")
      fields.append({
        "name": identifier_node["strg"],
        "value": integer_cst["int"]
      })
      if not "chan" in prm:
        break
      _, prm = traverse(chunk, prm, "chan")
    return fields

  found_enums = set()
  enum_data = []
  for chunk in chunks:
    for enum_declaration in find_nodes(chunk, "enumeral_type"):
      if not "name" in enum_declaration:
        continue
      name = enum_name(chunk, enum_declaration)
      if name in found_enums:
        continue
      found_enums.add(name)
      enum_data.append({
        "typename": name,
        "fields": enum_fields(chunk, enum_declaration)
      })
  return enum_data

def used_record_names(parsed_functions):
  record_names = set()
  for function in parsed_functions:
    return_data = function["returns"]
    if return_data["kind"] in ["record_type", "union_type"]:
      record_names.add((return_data["kind"], return_data["typename"]))
    for argument_data in function["arguments"]:
      if not argument_data["kind"] in ["record_type", "union_type"]:
        continue 
      record_names.add((argument_data["kind"], argument_data["typename"]))
  return record_names

def extract_pointers(chunks):
  found_pointers = set()
  pointer_data = []
  for chunk in chunks:
    pointer_declarations = find_nodes(chunk, "pointer_type")
    for pointer_declaration in pointer_declarations:
      typename = pointer_typename(chunk, "pointer_type", pointer_declaration)
      if typename in found_pointers:
        continue
      found_pointers.add(typename)
      kind, type_node = traverse(chunk, pointer_declaration, "ptd")
      underlying_data = extract_type(chunk, kind, type_node)
      if kind == "function_type":
        return_data, argument_data = extract_function_pointer(chunk, type_node)
        underlying_data = {**underlying_data, "returns": return_data, "arguments": argument_data}
      pointer_data.append({"typename": typename, "underlying": underlying_data})
  return pointer_data
    
def extract_struct(chunks, kind, typename):

  def check_owner(chunk, field_node):
    _, record_node = traverse(chunk, field_node, "scpe")
    record_node_idx = field_node["scpe"]
    typedef = not "name" in record_node 
    if typedef:
      nodes = find_nodes(chunk, "record_type") + find_nodes(chunk, "union_type")
      for node in nodes:
        if not "unql" in node or node["unql"] != record_node_idx:
          continue
        else:
          record_node = node 
          break 
    path = ["name", "name"] if typedef else ["name"]
    _, identifier_node = traverse(chunk, record_node, *path)
    return identifier_node["strg"] == typename.split()[-1] # compare with 'struct' or 'union' prefix removed

  found_field_names = set()
  record_fields = []
  for chunk in chunks:
    field_nodes = [field_node for field_node in find_nodes(chunk, "field_decl") if check_owner(chunk, field_node)]
    for field_node in field_nodes:
      field_name = traverse(chunk, field_node, "name")[1]["strg"]
      if field_name in found_field_names:
        continue
      found_field_names.add(field_name)
      field_offset = traverse(chunk, field_node, "bpos")[1]["int"]
      field_data = {"name": field_name, **extract_type(chunk, *traverse(chunk, field_node, "type"))}
      record_fields.append((field_data, field_offset))
  record_fields = [item[0] for item in sorted(record_fields, key=lambda p: p[1])] # sort by offset
  return {"kind": kind, "typename": typename, "fields": record_fields}

def function_arguments(chunk):
  decl_node = find_node(chunk, "function_decl")
  arguments = []
  _, prm = traverse(chunk, decl_node, "type", "prms")
  while "chan" in prm:
      arguments.append(extract_type(chunk, *traverse(chunk, prm, "valu")))
      _, prm = traverse(chunk, prm, "chan")
  return arguments

def make_node(line):
  if match := re.fullmatch(r"^@\d+ (?P<name>\w+) (?P<params>.*)$", line):
    traits = {}
    for arg, val in re.findall(r"([a-z]+) ?: ([^\s]+)", match.group("params")):
      if match_val := re.match(r"@(?P<id>\d+)", val):
        traits[arg] = int(match_val.group("id")) - 1
      else:
        traits[arg] = val
    return (match.group("name"), traits)
  else:
    raise ValueError(f"make_node: Could not process line '{line}'")

def chunks(lines):
  chunk = []
  for line in lines[2:]:
    if re.fullmatch(r"^;;.*$", line):
      if re.fullmatch(r"^;; Function.*$", line):
        yield chunk
      chunk = []
    else:
      node = make_node(line)
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
  parsed_ast = {"functions": [], "records": []}
  for file in args.infile:
    lines = [" ".join(line.split()) for line in file if not re.match(r"^\s+$", line)]
    lines = coalesce(lines)
    for chunk in chunks(lines): 
      name = function_name(chunk)
      return_data = return_type(chunk)
      arguments = function_arguments(chunk)
      function = {"name": name, "returns": return_data, "arguments": arguments}
      parsed_ast["functions"].append(function)
    for used_records in used_record_names(parsed_ast["functions"]):
      record_data = extract_struct(chunks(lines), *used_records)
      parsed_ast["records"].append(record_data)
    parsed_ast["pointers"] = extract_pointers(chunks(lines))
    parsed_ast["enums"] = extract_enums(chunks(lines))
  outfile.write(json.dumps(parsed_ast, indent=2))
  outfile.close()

if __name__ == "__main__":
  main()
