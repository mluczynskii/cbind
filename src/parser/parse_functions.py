import re
import os
import sys

def get_name(l):
    return l[l.find(" ", 11) + 1:l.find(" ", 12)]

def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line

def skip_to_nodes(f):
    while(not re.search("^@", peek_line(f))):
        f.readline()

def skip_empty(f):
    while(peek_line(f) == "\n"):
        f.readline()

def eof(f, size):
    return f.tell() == size

def get_file_size(file):
    pos = file.tell()
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(pos)
    return size

def parse_dict(d):
    for k in d.keys():
        vals = d[k]
        for i in range(len(vals)):
            if(re.search("^@", vals[i])):
                vals[i] = d[vals[i]][0]
    return d

#returns field value of given node
def retrieve_field(d, node_id, field):
    if field == "ptd:" or field == "ptd :" \
    or field == "tag:" or field == "tag :":
        field  = field[0:field.index(":")].strip()
        return d[node_id][d[node_id].index(field) + 2]
    else:
        return d[node_id][d[node_id].index(field) + 1]

#returns first col of node
def retrieve_node(d, node_id):
    return d[node_id][0]

#resolves fileds given in path and returns first col of node if last field value is node_id
def resolve_path(d, start, path):
    temp = start
    for field in path:
        temp = retrieve_field(d, temp, field)
    if temp[0] == '@':
        temp = retrieve_node(d, temp)
    return temp

def get_type_ids(d, node):
    res = []
    for k in d.keys():
        if d[k][0] == node:
            res.append(k)
    return res

def get_simple_type_entry(d, k):
    return {
                "name": resolve_path(d, k, ["name:", "strg:"]),
                "type": d[retrieve_field(d, k, "type:")][0],
                "type_name": resolve_path(d, k, ["type:", "name:", "name:", "strg:"])
            }

def collect_fptr_prms(d, k):
    #if function_type has prms: then arguments
    #are given on list of tree_list nodes, terminated by void_type
    #else no parameters are present
    #(d,k) -> type -> ptd -? 'prms' while tree_list has @chan
    #needs to be checked
    ptd_id = retrieve_field(d, retrieve_field(d, k, "type:"), "ptd:")
    if  'prms:' in d[ptd_id]:
        tree_list_id = retrieve_field(d, ptd_id, "prms:")
        prms = []
        while "chan:" in d[tree_list_id]:
            prms.append({
                    "type": resolve_path(d, tree_list_id, ["valu:"]),
                    "type_name": resolve_path(d, tree_list_id, ["valu:", "name:", "name:", "strg:"])
                })
            tree_list_id = retrieve_field(d, tree_list_id, "chan:")
        return prms
    else:
        return []

def get_pointer_type_entry(d, k):
    ptd = resolve_path(d, k, ["type:", "ptd:"])
    if ptd == 'function_type':
        info = {
            "return_expr": {
                "type": resolve_path(d, k, ["type:", "ptd:", "retn:"]),
                "type_name": resolve_path(d, k, ["type:", "ptd:", "retn:", "name:", "name:", "strg:"])
                },
            "args": collect_fptr_prms(d, k)
            }
        res = {
                "name": resolve_path(d, k, ["name:", "strg:"]),
                "type": "fptr_type",
                "info": info
            }
        return res
    else:
        return {
                    "name": resolve_path(d, k, ["name:", "strg:"]),
                    "type": d[retrieve_field(d, k, "type:")][0],
                    "type_name": resolve_path(d, k, ["type:", "ptd:", "name:", "name:", "strg:"]) + "ptr_type"
                }


def get_struct_fields(d, k):
    record = retrieve_field(d, k, "type:")
    res = []
    for key in d.keys():
        if retrieve_node(d, key) == "field_decl":
            if retrieve_field(d, key, "scpe:") == record:
                res.append(get_arg(d, key))
    return res


def get_struct_type_entry(d, k):
    res = {
        "name": resolve_path(d, k, ["name:", "strg:"]),
        "type": resolve_path(d, k, ["type:", "tag :"]),
        "type_name": resolve_path(d, k, ["type:", "name:", "strg:"]),
        "fields": get_struct_fields(d, k)
    }

    return res


def get_arg(d, k):
    argType = d[retrieve_field(d, k, "type:")][0]
    if argType == "integer_type":
        return get_simple_type_entry(d, k)
    elif argType == "pointer_type":
        return get_pointer_type_entry(d, k)
    elif argType == "record_type":
        return get_struct_type_entry(d, k)


def simplify_dict(d):
    new_dict = {}
    try:
        new_dict["name"] = d["@0"][0]
    except:
        new_dict["name"] = None
    try:
        new_dict["return_expr"] = {
            "type": resolve_path(d, get_type_ids(d, "return_expr")[0], ["expr:", "type:"]),
            "type_name": resolve_path(d, get_type_ids(d, "return_expr")[0], ["expr:", "type:", "name:", "name:", "strg:"]),
            }
    except:
        new_dict["return_expr"] = {
            "type": None,
            "type_name": None
            }
    new_dict["args"] = []
    for k in get_type_ids(d, "parm_decl"):
        try:
            # Checking if param k is in function signature
            if "scpe:" in d[k] and resolve_path(d, k, ["scpe:", "name:", "strg:"]) == d["@0"][0]:
                new_dict["args"].append(get_arg(d, k))
        except ValueError as err:
            print(f'Could not append arg {k} of {d["@0"][0]}.\n{err}', file=sys.stderr)
        except Exception as exc:
            print(exc, file=sys.stderr) 
        # new_dict["args"].append(get_arg(d, k))
    return new_dict

def validate_file(file):
    skip_empty(file)
    return re.search("^;; Function", peek_line(file)) != None

def run_parser(file):
    file_size = get_file_size(file)
    skip_empty(file)
    res = []
    while(re.search("^;; Function", peek_line(file))):
        dict = {}
        name = get_name(file.readline())
        dict["@0"] = [name]
        skip_to_nodes(file)
        while(not (re.search("^;; Function", peek_line(file)) or eof(file, file_size))):
            node = file.readline()
            while(not (re.search("^@|^;; Function", peek_line(file)) or peek_line(file) == "\n")):
                node += file.readline()
                skip_empty(file)
            node = node.split()
            skip_empty(file)
            dict[node[0]] = node[1:]
        # print(simplify_dict(dict))
        res.append(simplify_dict(dict))
    return res
