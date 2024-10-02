from lib.components import *
from lib.structs import StructHandler
from lib.callbacks import CallbackHandler
from typing import Tuple

STORAGE_SIZE = 20

class FunctionHandler():
    functionInfo: dict 

    def __init__(self, data: list, structHandler: StructHandler) -> None:
        self.functionInfo = {}
        for function in data:
            name = function['name']
            returnType = parseType(function['return_expr']['type_name'])
            arguments = function['args']

            apiCallArgList, externArgList = [], []
            wrapperCode = Sequence()
            returnCount = 1

            for idx, arg in enumerate(arguments):
                argumentKind = arg['type']
                argumentTypeName = arg.get('type_name', None)
                argName = arg['name']
                if argumentKind == 'fptr_type':
                    code, component = FunctionHandler.fptrCode(arg, idx+1)
                elif argumentKind == 'struct':
                    code, component = FunctionHandler.structCode(structHandler, arg, idx+1, False)
                elif argumentKind == 'structptr_type':
                    code, component = FunctionHandler.structCode(structHandler, arg, idx+1, True)
                elif argumentTypeName in ['char', 'char*']:
                    code, component = FunctionHandler.charCode(arg, idx+1)
                elif argumentKind in ['integer_type', 'real_type']:
                    code, component = FunctionHandler.simpleCode(arg, idx+1)
                else:
                    raise NotImplementedError(f'Unhandled argument type: {argumentTypeName}')
                
                if argumentTypeName == 'char' or argumentKind == 'struct':
                    apiCallArgList.append(f'*{argName}')
                else:
                    apiCallArgList.append(argName)
                externArgList.append(component)
                wrapperCode = wrapperCode + code 

            apiCall = FunctionCall(name, apiCallArgList)
            if returnType != Type.VOID:
                result = Variable(returnType, 'result', value=apiCall)
                pushFunction = stackPushPop(returnType, Direction.PUSH)
                pushArguments = ['state', '&result', 1] if function['return_expr']['type_name'] == 'char' else ['state', 'result']
                push = FunctionCall(pushFunction, pushArguments)
                wrapperCode = wrapperCode + result + push
            else:
                returnCount = returnCount - 1
                wrapperCode = wrapperCode + apiCall 
            
            declaration = Function(returnType, name, externArgList, Modifier.EXTERN)
            wrapperName = f'c_{name}'
            wrapper = Function(
                Type.INTEGER,
                wrapperName, 
                [Variable(Type.STATE, 'state')],
                content=wrapperCode + Return(returnCount)
            )
            self.functionInfo[name] = {
                'wrapperName': wrapperName,
                'wrapper': wrapper,

                'declaration': declaration
            }

    @staticmethod 
    def simpleCode(arg: dict, idx: int) -> Tuple[Sequence, Variable]:
        argType = parseType(arg['type_name'])
        pop = stackPushPop(argType, Direction.POP)
        var = Variable(
            argType,
            arg['name'],
            value=FunctionCall(pop, ['state', idx])
        )
        code = Sequence(var)
        return code, Variable(argType, arg['name'])
                    
    @staticmethod 
    def structCode(structHandler: StructHandler, arg: dict, idx: int, ptr: bool) -> Tuple[Sequence, Component]:
        structName = arg['type_name']
        return structHandler.unpackStruct(arg['name'], structName, idx, ptr) 

    @staticmethod 
    def charCode(arg: dict, idx: int) -> Tuple[Sequence, Variable]:
        component = Variable(
            Type.STRING,
            arg['name'],
            value=FunctionCall('lua_tostring', ['state', idx])
        )
        code = Sequence(component)
        return code, Variable(Type.CHAR if arg['type_name'] == 'char' else Type.STRING, arg['name'])

    @staticmethod 
    def fptrCode(arg: dict, idx: int) -> Tuple[Sequence, FunctionPointer]:
        code = Sequence()
        code = code + FunctionCall('lua_pushvalue', ['state', idx])
        registryKey = Variable(
            Type.INTEGER,
            'registry_key',
            value=FunctionCall(
                'luaL_ref',
                ['state', 'LUA_REGISTRYINDEX']
            )
        )
        data = Struct(
            'container',
            'data',
            pointer=True,
            value=Casting(
                'struct container*',
                FunctionCall(
                    'malloc',
                    ['sizeof(struct container)']
                )
            )
        )
        code = code + registryKey + data 

        setState = StructAssign('data', 'state', 'state', pointer=True)
        setRegistryKey = StructAssign('data', 'registry_key', 'registry_key', pointer=True)
        code = code + setState + setRegistryKey 

        fptrInfo = arg['info']
        returnType = parseType(fptrInfo['return_expr']['type_name'])
        argTypes = [parseType(x['type_name']) for x in fptrInfo['args']]
        helperName = CallbackHandler.callbackWrapperName(fptrInfo)
        fptr = FunctionPointer(returnType, arg['name'], argTypes)
        closure = Closure(fptr, helperName, 'data')
        code = code + closure
        code = code + ArrayAssign('callbackStorage', 'storageIdx', arg['name']) + ArrayAssign('dataStorage', 'storageIdx', 'data') + Increment('storageIdx')
        return code, fptr
    
    @staticmethod
    def defineCallbackStorage() -> Sequence:
        fptrStorage = Variable(
            Type.VOID_PTR, 
            'callbackStorage',
            array=True,
            size=STORAGE_SIZE
        )
        dataStorage = Variable(
            Type.VOID_PTR,
            'dataStorage',
            array=True,
            size=STORAGE_SIZE 
        )
        idx = Variable(Type.INTEGER, 'storageIdx', value=0)
        return Sequence(fptrStorage, dataStorage, idx)

    def declareFunctions(self) -> Sequence:
        seq = Sequence()
        for function in self.functionInfo.values():
            seq = seq + function['declaration']
        return seq
    
    def defineWrappers(self) -> Sequence:
        seq = Sequence()
        for function in self.functionInfo.values():
            seq = seq + function['wrapper']
        return seq 

    def defineRegister(self) -> LuaRegister:
        functions = {}
        for name, info in self.functionInfo.items():
            functions[name] = info['wrapperName'] 
        return LuaRegister('luareg', functions) 
