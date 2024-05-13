from lib.components import *
from lib.callbacks import CallbackHandler
from lib.structs import StructHandler

class FunctionHandler():
    functionInfo: dict 

    def __init__(self, data: dict, structHandler: StructHandler) -> None:
        self.functionInfo = {}
        for function in data:
            if function['return_expr']['type'] != 'integer_type':
                continue
            externArgList, apiCallArgList = [], []
            wrapperCode = Sequence()
            for i, arg in enumerate(function['args']):
                if arg['type'] == 'fptr_type':
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
                elif arg['type'] == 'struct':
                    structName = arg['type_name']
                    externArgList.append(f'struct {structName} {arg["name"]}')

                    unpack = structHandler.unpackStruct(structName, i+1)
                    apiCallArgList.append(f'arg{i+1}')
                    wrapperCode = wrapperCode + unpack 
                elif arg['type'] == 'integer_type':
                    externArgList.append(f'{arg["type_name"]} {arg["name"]}')

                    x = Variable(
                        'int',
                        f'arg{i+1}',
                        value=FunctionCall('lua_tonumber', ['L', i+1])
                    )
                    apiCallArgList.append(f'arg{i+1}')
                    wrapperCode = wrapperCode + x
                else:
                    break 
            else:
                declaration = Function(
                    function['return_expr']['type_name'],
                    function['name'],
                    externArgList, 
                    modifier=Modifier.EXTERN
                )
                apicall = FunctionCall(
                    function['name'],
                    apiCallArgList
                )
                wrapperCode = wrapperCode + FunctionCall('lua_pushinteger', ['L', apicall], semicolon=True) + Return(1)
                wrapper = Function(
                    'int', 
                    f'c_{function["name"]}', 
                    ['lua_State* L'],
                    seq=wrapperCode 
                )
                self.functionInfo[function['name']] = {
                    'declaration': declaration,
                    'wrapper': wrapper  
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
        xs = [name for name in self.functionInfo]
        return LuaRegister('luareg', xs) 
