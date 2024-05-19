from lib.luaComponents import *
from lib.functions import FunctionHandler

class LuaFunctionHandler():
    luaFunctionInfo: dict 

    def __init__(self, functionHandler: FunctionHandler) -> None:
        self.functionInfo = {}
        for apiName, info in functionHandler.functionInfo.items():
            referenceIndex = info['references'] 
            if len(referenceIndex) == 0:
                continue
            argCount = info['argCount'] 
            intermediateApiName = info['intermediateName']
            arglist = [f'arg{i+1}' for i in range(argCount)]

            wrapperCode = LuaSequence()

            apiCall = LuaCallApi(
                'CFunction', 
                intermediateApiName,
                arglist,
                referenceIndex,
                info['void']
            )
            wrapperCode = wrapperCode + apiCall 

            for idx in referenceIndex:
                copy = LuaCopyStruct(f'narg{idx}', f'arg{idx}')
                wrapperCode = wrapperCode + copy 

            if not info['void']:
                wrapperCode = wrapperCode + LuaReturn('value')
            wrapper = LuaFunction(
                f'CFunction.{apiName}',
                arglist,
                wrapperCode 
            )
            self.functionInfo[apiName] = wrapper 

    def defineWrappers(self) -> LuaSequence:
        seq = LuaSequence()
        for _, wrapper in self.functionInfo.items():
            seq = seq + wrapper 
        return seq 

