from lib.components import *

class CallbackHandler():
    callbacksInfo: dict

    def __init__(self, data: dict) -> None:
        self.callbacksInfo = {}
        for f in data:
            for arg in f['args']:
                if arg['type'] != 'fptr_type':
                    continue
                info = arg['info']
                name = CallbackHandler.callbackWrapperName(info)
                wrapper = CallbackHandler.callbackWrapper(info, name)
                self.callbacksInfo[name] = wrapper 

    @staticmethod
    def callbackWrapperName(info: dict) -> str:
        return_ = info["return_expr"]["type_name"]
        args = ''.join( [arg["type_name"] for arg in info["args"]] )
        return f'{return_}_{args}'
    
    @staticmethod
    def callbackWrapper(info: dict, name: str) -> Function:
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
    
    def defineCallbacks(self) -> Sequence:
        seq = Sequence()
        for wrapper in self.callbacksInfo.values():
            seq = seq + wrapper 
        return seq
                