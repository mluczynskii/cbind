SIMPLE = ["integer_type", "character_type", "real_type"]

STACK_INSTR = {
  "integer_type": ["lua_tointeger", "lua_pushinteger"],
  "real_type": ["lua_tonumber", "lua_pushnumber"],
  "character_type": ["lua_tostring", "lua_pushlstring"]
}

def stack_pop(kind, stack_idx):
  call = f"{STACK_INSTR[kind][0]}(state, {stack_idx})"
  if kind == "character_type":
    call = f"{call}[0]"
  return call
  
def stack_push(kind, var_name):
  call = f"{STACK_INSTR[kind][1]}(state"
  if kind == "character_type":
    return f"(void){call}, &{var_name}, 1)"
  return f"{call}, {var_name})"
  
def format_fptr(arg):
  fptr_arguments = [x["Typename"] for x in arg["Pointer"]["Arguments"]]
  return_type = arg["Pointer"]["Returns"]["Typename"]
  return f"{return_type} (*{arg["Name"]})({', '.join(fptr_arguments)})"

def format_variable(arg):
  if arg["Kind"] == "record_type" and not arg["Typedef"]:
    return f"struct {arg["Typename"]} {arg["Name"]}"
  elif arg["Kind"] in SIMPLE or arg["Kind"] == "record_type":
    return f"{arg["Typename"]} {arg["Name"]}"
  elif arg["Kind"] == "pointer_type":
    if "Returns" in arg["Pointer"]:
      return format_fptr(arg)
    return f"{arg["Pointer"]["Typename"]} *{arg["Name"]}"

def fetch_arguments(args):
  code = []
  for index, arg in enumerate(args):
    fetch = stack_pop(arg["Kind"], index + 1)
    variable = format_variable(arg)
    code.append(f"{variable} = {fetch};")
  return "\n".join(code)

def call_api(function):
  arg_names = [arg["Name"] for arg in function["Arguments"]]
  call = f"{function["Name"]}({", ".join(arg_names)});"
  if function["Returns"]["Kind"] != "void_type": 
    result = format_variable({**function["Returns"], "Name": "result"})
    call = f"{result} = {call}"
  return call

def create_wrapper(function):
  signature = f"int c_{function["Name"]}(lua_State *state)"
  preparation = fetch_arguments(function["Arguments"])
  apicall = call_api(function)
  body = [preparation, apicall]
  if function["Returns"]["Kind"] != "void_type":
    push = stack_push(function["Returns"]["Kind"], "result")
    body.append(f"{push};")
  body.append("return 1;" if function["Returns"]["Kind"] != "void_type" else "return 0;")
  return {"Signature": signature, "Body": body}
  
