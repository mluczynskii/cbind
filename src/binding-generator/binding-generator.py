from components import *
import json
import argparse 
import boilerplate

HEADERS = [
    "lua.h",
    "lualib.h",
    "lauxlib.h"
]

usedWrapperNames = {}

def loadInfo(filename):
    with open(filename, 'r') as input:
        data = json.load(input)
    return data

def writeHeaders(file):
    for header in [Include(lib, True) for lib in HEADERS]:
        file.write(f'{header}\n') 
    file.write('\n')

def writeBoilerplate(file):
    file.write(boilerplate.code + '\n')

def writeDeclarations(file, data):
    for function in data:
        arglist = []
        for i, arg in enumerate(function["args"]):
            if arg["type"] == 'fptr_type':
                info = arg["info"]
                fptr = FunctionPointer(
                    info["return_expr"]["type_name"],
                    f'arg{i+1}',
                    [x["type_name"] for x in info["args"]]
                )
                arglist.append(str(fptr))
            else:
                arglist.append(f'{arg["type_name"]} arg{i+1}')

        declaration = Function(
            function["return_expr"]["type_name"],
            function["name"],
            arglist, 
            modifier=Modifier.EXTERN
        )

        file.write(f'{declaration}\n');
    file.write('\n');

def writeContext(file):
    definition = Struct(
        'context',
        [Variable('lua_State*', 'stack'), Variable('int', 'idx')]
    )
    declaration = Variable('struct context', 'c')
    file.write(f'{definition}\n{declaration}\n\n')

# Generates a name for a callback wrapper based on it's type
def callbackWrapperName(info):
    return_ = info["return_expr"]["type_name"]
    args = ''.join( [arg["type_name"] for arg in info["args"]] )
    return f'{return_}_{args}'

# Generates a wrapper that allows to callback to lua functions
def callbackWrapper(info, name):
    args = [f'{arg["type_name"]} arg{i+1}' for i, arg in enumerate(info["args"])]

    content = Sequence()
    content = content + FunctionCall('lua_pushvalue', ['c.stack', 'c.idx'], semicolon=True)

    for i in range(len(args)):
        pushArg = FunctionCall(
            'lua_pushinteger', 
            ['c.stack', f'arg{i+1}'], 
            semicolon=True
        )
        content = content + pushArg

    pcall = FunctionCall(
        'lua_pcall', 
        ['c.stack', len(args), 1, 0], 
        semicolon=True
    )
    pop = FunctionCall(
        'lua_tonumber', 
        ['c.stack', -1]
    )
    content = content + pcall + Return(pop)
    return Function(info["return_expr"]["type_name"], name, args, seq=content)

# Writes wrappers for API functions and required callback types to file
def writeWrappers(file, data):
    for function in data:
        content = Sequence()
        arglist = []
        for i, arg in enumerate(function["args"]):
            if arg["type"] == 'fptr_type':
                name = callbackWrapperName(arg["info"])
                if name not in usedWrapperNames:
                    usedWrapperNames[name] = True
                    wrapper = callbackWrapper(arg["info"], name);
                    file.write(f'{wrapper}\n\n')
                arglist.append(f'&{name}')
                content = content + ContextChange(i+1);
            else:
                x = Variable(
                    "int",
                    f'arg{i+1}',
                    value=FunctionCall('lua_tonumber', ['L', i+1])
                )
                arglist.append(f'arg{i+1}')
                content = content + x

        apicall = FunctionCall(
            function["name"],
            arglist
        )

        content = content + FunctionCall('lua_pushinteger', ['L', apicall], semicolon=True) + Return(1)

        wrapper = Function(
            'int', 
            f'c_{function["name"]}', 
            ['lua_State* L'],
            seq=content
        )

        file.write(f'{wrapper}\n\n')

def writeRegister(file, data):
    xs = [f["name"] for f in data]
    register = LuaRegister("luareg", xs)
    file.write(f'{register}\n\n')

def main():
    parser = argparse.ArgumentParser(
        prog="binding-generator",
        description="Generates binding file based on C API AST dump."
    )
    parser.add_argument("inputfile")
    parser.add_argument("outputfile")
    args = parser.parse_args()

    data = loadInfo(args.inputfile)
    with open(args.outputfile, 'w') as output:
        output.write("// Generated by binding-generator.py \n")
        writeHeaders(output)
        writeContext(output)
        writeDeclarations(output, data)
        writeWrappers(output, data)
        writeRegister(output, data)
        output.write("// Boilerplate code \n")
        writeBoilerplate(output)

if __name__ == '__main__':
    main()