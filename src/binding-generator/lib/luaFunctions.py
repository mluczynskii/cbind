from lib.luaComponents import *
from lib.functions import FunctionHandler

class LuaFunctionHandler():
    luaFunctionInfo: dict 

    def __init__(self, functionHandler: FunctionHandler) -> None:
        self.functionInfo = {}
        for apiName, info in functionHandler.functionInfo.items():
            wrapperName = info['wrapperName'] 
            argCount = info['argCount'] 
            referenceIndex = info['references'] 
            arglist = [f'arg{i+1}' for i in range(argCount)]

            wrapperCode = LuaSequence()

            apiCall = LuaCallApi(
                'CFunction', 
                wrapperName,
                arglist,
                referenceIndex
            )
            wrapperCode = wrapperCode + apiCall 

            for idx in refenceIndex:
                copy = LuaCopyStruct(f'narg{idx}', f'arg{idx}')
                wrapperCode = wrapperCode + copy 

            wrapperCode = wrapperCode + LuaReturn('value')
            wrapper = LuaFunction(
                'CFunction',
                arglist,
                wrapperCode 
            )
            self.functionInfo[apiName] = wrapper 

    def defineWrappers(self) -> LuaSequence:
        seq = LuaSequence()
        for _, wrapper in self.functionInfo.items():
            seq = seq + wrapper 
        return seq 

