# v0.0.2 - a lot of hacks...
from components import *
import json
import argparse 
import boilerplate

HEADERS = [
    "lua.h",
    "lualib.h",
    "lauxlib.h"
];

def load_info(filename):
    f = open(filename, 'r');
    data = json.load(f);
    f.close();
    return data;

def write_headers(file):
    for header in [Include(h, True) for h in HEADERS]:
        file.write(str(header)); 
    file.write('\n');

def write_boilerplate(file):
    file.write(boilerplate.code + '\n');

def write_declarations(file, data):
    for function in data:
        arglist = [
            f'{arg["type_name"]} arg{i+1}' for i, arg in enumerate(function["args"])
        ];

        f = Function(
            function["return_expr"]["type_name"],
            function["name"],
            arglist, 
            modifier=Modifier.EXTERN
        );

        file.write(str(f) + '\n');

# TODO: So far it only works with functions returning int and taking int arguments
def write_wrappers(file, data):
    for function in data:
        argcount = len(function["args"]);

        # int arg1 = lua_tonumber(L, 1); [...]
        prefix = Block([
            Variable(
                False,
                "int",
                f'arg{i}',
                False,
                value=FunctionCall('lua_tonumber', ['L', i])
            ) for i in range(1, argcount+1)
        ]);

        apicall = FunctionCall(
            function["name"],
            [f'arg{i}' for i in range(1, argcount+1)]
        );

        # lua_pushinteger(L, api_name(arg1, ..., argn));
        # return 1;
        suffix = Block([
            FunctionCall('lua_pushinteger', ['L', apicall], last=True),
            Return(1)
        ]);

        # everything put together
        f = Function(
            "int", 
            f'c_{function["name"]}', 
            ["lua_State* L"],
            content=Block.merge(prefix,suffix)
        );

        file.write(str(f) + '\n');

def write_register(file, data):
    xs = ['{' + f'"{fun["name"]}", c_{fun["name"]}' + '}' for fun in data];

    register = Variable(
        True,
        "luaL_Reg",
        "luareg",
        True,
        modifier=Modifier.CONST,
        value=Block([ListInitializer(xs)])
    );
    file.write(str(register) + ';\n');

def main():
    parser = argparse.ArgumentParser(
        prog="binding-generator",
        description="Generates binding file based on C API AST dump."
    );
    parser.add_argument("inputfile");
    parser.add_argument("outputfile");
    args = parser.parse_args();

    data = load_info(args.inputfile);
    with open(args.outputfile, 'w') as output:
        output.write("// Generated by binding-generator.py \n");
        write_headers(output);
        write_declarations(output, data);
        write_wrappers(output, data);
        write_register(output, data);
        write_boilerplate(output);

if __name__ == '__main__':
    main();