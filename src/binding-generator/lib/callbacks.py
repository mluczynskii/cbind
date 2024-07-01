from lib.components import *

def va_suffix(type_: Type) -> str:
    if type_ in [Type.CHAR, Type.DOUBLE, Type.FLOAT, Type.INTEGER, Type.LONG, Type.SHORT, Type.VOID]:
        return type_.value
    raise NotImplementedError(f'Unhandled return type: {type_.value}')

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
        return_ = info['return_expr']['type_name']
        args = ''.join( [arg['type_name'] for arg in info['args']] )
        return f'{return_}_{args}'
    
    @staticmethod
    def callbackWrapper(info: dict, name: str) -> Function:
        argTypes = [parseType(arg['type_name']) for arg in info['args']]
        returnType = parseType(info['return_expr']['type_name'])

        content = Sequence()

        container = Struct(
            'container',
            'c',
            pointer=True,
            value=Casting('struct container*', 'data')
        )
        content = content + container 

        registryKey = Variable(
            Type.INTEGER,
            'registry_key',
            value=StructAccess('c', 'registry_key')
        )
        state = Variable(
            Type.STATE,
            'state',
            value=StructAccess('c', 'state')
        )
        content = content + registryKey + state 

        # callback fetching from the lua register
        fpush = FunctionCall(
            'lua_rawgeti',
            ['state', 'LUA_REGISTRYINDEX', 'registry_key']
        )
        content = content + fpush

        # argument fetching
        typeSuffix = va_suffix(returnType)
        start = FunctionCall(f'va_start_{typeSuffix}', ['args'])
        content = content + start
        for idx, argType in enumerate(argTypes):
            argTypeSuffix = va_suffix(argType)
            fetch = FunctionCall(f'va_arg_{argTypeSuffix}', ['args'])
            argument = Variable(argType, f'arg{idx}', value=fetch)
            content = content + argument

        # argument pushing 
        for idx, argType in enumerate(argTypes):
            push = stackPushPop(argType, Direction.PUSH)
            content = content + FunctionCall(push, ['state', f'arg{idx}'])

        pcall = FunctionCall('lua_pcall', ['state', len(argTypes), 1, 0])
        popFunction = stackPushPop(returnType, Direction.POP)
        pop = FunctionCall(popFunction, ['state', -1])
        result = Variable(returnType, 'result', value=pop)
        end = FunctionCall(f'va_return_{typeSuffix}', ['args', 'result'])
        content = content + pcall + result + end + Return('result')

        data = Variable(Type.VOID_PTR, 'data')
        args = Variable(Type.VA_LIST, 'args')
        wrapper = Function(
            returnType,
            name,
            [data, args],
            content=content
        )
        return wrapper
    
    def defineCallbacks(self) -> Sequence:
        seq = Sequence()
        for wrapper in self.callbacksInfo.values():
            seq = seq + wrapper 
        return seq
                