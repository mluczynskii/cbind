from lib.components import *
from lib.structs import StructHandler 
from lib.callbacks import CallbackHandler
from lib.functions import FunctionHandler
from lib.luaFunctions import LuaFunctionHandler

import json
import argparse 
import boilerplate

HEADERS = [
    "lua.h",
    "lualib.h",
    "lauxlib.h",
    "callback.h",
    "stdlib.h"
]

# loads .json AST dump into a python dictionary for further use
def loadInfo(filename):
    with open(filename, 'r') as input:
        data = json.load(input)
    return data

def writeHeaders(file):
    for header in [Include(lib, True) for lib in HEADERS]:
        file.write(f'{header}\n') 
    file.write('\n')

# initLua, execScript and closeLua functions
def writeBoilerplate(file):
    file.write(boilerplate.code + '\n')

# lua_Reg structure that exposes wrappers to Lua
def writeRegister(file, functionHandler):
    register = functionHandler.defineRegister()
    file.write(f'{register}\n\n')

# writes wrappers into .lua binding file that is used to call API functions using struct pointers 
def writeLuaWrappers(luaFile, luaFunctionHandler):
    wrappers = luaFunctionHandler.defineWrappers()
    luaFile.write(str(wrappers))

# write extern declarations of the targeted C API, along with needed type declarations
def writeDeclarations(file, structHandler, functionHandler):
    storage = FunctionHandler.defineCallbackStorage()
    file.write(f'{storage}\n\n')

    structDeclarations = structHandler.declareStructs()
    file.write(f'{structDeclarations}\n\n')
    constructors = structHandler.declareConstructors()
    file.write(f'{constructors}\n\n')
    setters = structHandler.declareSetters()
    file.write(f'{setters}\n\n')
    getters = structHandler.declareGetters()
    file.write(f'{getters}\n\n')

    functionDeclarations = functionHandler.declareFunctions()
    file.write(f'{functionDeclarations}\n\n')

# write wrappers for needed callbacks and API functions
def writeWrappers(file, callbackHandler, functionHandler):
    callbackCallers = callbackHandler.defineCallbacks()
    file.write(f'{callbackCallers}\n\n')

    functionWrappers = functionHandler.defineWrappers()
    file.write(f'{functionWrappers}\n\n')

def main():
    parser = argparse.ArgumentParser(
        prog='binding-generator',
        description='Generates binding file based on C API AST dump.'
    )
    parser.add_argument('input_file', help='Name of .json file produced by the AST parser')
    parser.add_argument('-o', '--output', help='Name of output .c and .lua files (without extension), default is "binding"')
    args = parser.parse_args()

    data = loadInfo(args.input_file)

    structHandler = StructHandler(data)
    callbackHandler = CallbackHandler(data)
    functionHandler = FunctionHandler(data, structHandler)
    #luaFunctionHandler = LuaFunctionHandler(functionHandler)

    outputName = 'binding' if not args.output else args.output
    outputName = outputName.strip()
    with open(f'{outputName}.c', 'w') as output:
        writeHeaders(output)
        writeDeclarations(output, structHandler, functionHandler)
        writeWrappers(output, callbackHandler, functionHandler)
        writeRegister(output, functionHandler)
        writeBoilerplate(output)

    #if luaFunctionHandler.needWrappers():
     #   with open(f'{outputName}.lua', 'w') as luaOutput:
      #      writeLuaWrappers(luaOutput, luaFunctionHandler)

if __name__ == '__main__':
    main()