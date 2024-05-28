from lib.components import *
from lib.callbacks import CallbackHandler
from lib.structs import StructHandler

PUSH_FUNCTIONS = {
    'int': 'lua_pushinteger',
    'float': 'lua_pushnumber',
    'double': 'lua_pushnumber',
    'long': 'lua_pushinteger',
    'short': 'lua_pushinteger'
}

POP_FUNCTIONS = {
    'int': 'lua_tointeger',
    'float': 'lua_tonumber',
    'double': 'lua_tonumber',
    'long': 'lua_tointeger',
    'short': 'lua_tointeger'
}

class FunctionHandler():
    functionInfo: dict 

    def __init__(self, data: dict, structHandler: StructHandler) -> None:
        self.functionInfo = {}
        for function in data:
            if function['srcp'] != 'main.c' and function['srcp'] != 'string.h':
                continue
            returnType = function['return_expr']['type']
            externArgList, apiCallArgList = [], []
            wrapperCode, afterCallCode = Sequence(), Sequence()
            returnCount = 1
            referenceIndex = []
            argCount = len(function['args'])
            for i, arg in enumerate(function['args']):
                type_ = arg['type']
                if type_ == 'fptr_type':
                    info = arg['info']
                    fptr = FunctionPointer(
                        info['return_expr']['type_name'],
                        arg['name'],
                        [x['type_name'] for x in info['args']]
                    )
                    externArgList.append(str(fptr))

                    callbackWrapperName = CallbackHandler.callbackWrapperName(arg['info'])
                    apiCallArgList.append(f'&{callbackWrapperName}')
                    wrapperCode = wrapperCode + ContextChange(i+1)
                elif type_ == 'struct':
                    structName = arg['type_name']
                    externArgList.append(f'struct {structName} {arg["name"]}')

                    unpack = structHandler.unpackStruct(structName, i+1)
                    apiCallArgList.append(f'arg{i+1}')
                    wrapperCode = wrapperCode + unpack 
                elif type_ == 'structptr_type':
                    referenceIndex.append(i+1)
                    structName = arg['type_name']
                    externArgList.append(f'struct {structName}* {arg["name"]}')

                    unpack = structHandler.unpackStruct(structName, i+1)
                    apiCallArgList.append(f'&arg{i+1}')
                    wrapperCode = wrapperCode + unpack

                    pack = structHandler.packStruct(structName, i+1)
                    afterCallCode = afterCallCode + pack 
                    returnCount = returnCount + 1
                elif arg['type_name'] in PUSH_FUNCTIONS:
                    argType = arg['type_name']
                    externArgList.append(f'{argType} {arg["name"]}')

                    popFunction = POP_FUNCTIONS[argType]

                    x = Variable(
                        argType,
                        f'arg{i+1}',
                        value=FunctionCall(popFunction, ['L', i+1])
                    )
                    apiCallArgList.append(f'arg{i+1}')
                    wrapperCode = wrapperCode + x
                elif arg['type_name'] in ['char*', 'char']:
                    argType = arg['type_name']
                    externArgList.append(f'{argType} {arg["name"]}')

                    x = Variable(
                        'char*',
                        f'arg{i+1}',
                        value=FunctionCall('lua_tostring', ['L', i+1])
                    )
                    wrapperCode = wrapperCode + x
                    apiCallArg = f'arg{i+1}'
                    if argType == 'char':
                        apiCallArg = f'*{apiCallArg}'
                    apiCallArgList.append(apiCallArg)
                else:
                    break 
            else:
                apicall = FunctionCall(
                    function['name'],
                    apiCallArgList
                )

                if returnType == None:
                    returnCount = returnCount - 1
                    returnTypeName = 'void'
                    apicall.semicolon = True 
                    wrapperCode = wrapperCode + apicall
                else:
                    returnTypeName = function['return_expr']['type_name']
                    result = Variable(
                        returnTypeName,
                        'result',
                        value=apicall 
                    )
                    res = 'result'
                    if returnTypeName in PUSH_FUNCTIONS:
                        pushFunction = PUSH_FUNCTIONS[returnTypeName]
                    elif returnTypeName in ['char*', 'char']:
                        pushFunction = 'lua_pushstring'
                        if returnTypeName == 'char':
                            res = f'&{res}'
                    wrapperCode = wrapperCode + result + FunctionCall(pushFunction, ['L', res], semicolon=True) 
                
                declaration = Function(
                    returnTypeName,
                    function['name'],
                    externArgList, 
                    modifier=Modifier.EXTERN
                )

                wrapperCode = wrapperCode + afterCallCode + Return(returnCount)

                wrapperName = f'c_{function["name"]}'
                intermediateApiName = function['name']
                if len(referenceIndex) > 0:
                    intermediateApiName = f'{function["name"]}_ptr'
                    wrapperName = wrapperName + '_ptr'

                wrapper = Function(
                    'int', 
                    wrapperName, 
                    ['lua_State* L'],
                    seq=wrapperCode 
                )
                self.functionInfo[function['name']] = {
                    'intermediateName': intermediateApiName,
                    'wrapperName': wrapperName, 
                    'argCount': argCount,
                    'references': referenceIndex,
                    'declaration': declaration,
                    'wrapper': wrapper,
                    'void': returnTypeName == 'void'
                }

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
        for apiName, info in self.functionInfo.items():
            functions[info['intermediateName']] = info['wrapperName'] 
        return LuaRegister('luareg', functions) 
