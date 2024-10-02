from lib.components import *
from typing import Tuple

class StructHandler():
    structsInfo: dict 

    def __init__(self, data: dict) -> None:
        self.structsInfo = {}
        for f in data:
            for arg in f['args']:
                if arg['type'] not in ['struct', 'structptr_type'] :
                    continue
                fields = [Variable(parseType(x['type_name']), x['name']) for x in arg['fields']]
                struct = StructDefinition(arg['type_name'], fields)
                self.structsInfo[arg['type_name']] = struct 

    def unpackStruct(self, varName: str, typeName: str, stackIdx: int, pointer: bool) -> Tuple[Sequence, Component]:
        component = Struct(typeName, varName, pointer=pointer)
        code = Sequence(Struct(
            typeName,
            varName,
            pointer=True,
            value=Casting(
                f'struct {typeName} *',
                FunctionCall('lua_touserdata', ['state', stackIdx])
            )
        ))
        return code, component 

    def declareConstructors(self) -> Sequence:
        constructors = Sequence()
        for typeName, definition in self.structsInfo.items():
            code = Sequence()
            code = code + Variable( 
                Type.SIZE,
                'nbytes',
                value=FunctionCall('sizeof', [f'struct {typeName}'])
            )
            code = code + Struct(
                typeName,
                'result',
                pointer=True,
                value=Casting(
                    f'struct {typeName} *',
                    FunctionCall('lua_newuserdata', ['state', 'nbytes'])
                )
            )
            for idx, field in enumerate(definition.fields):
                code = code + StructAssign(
                    'result',
                    field.name,
                    value=FunctionCall(
                        stackPushPop(field.type_, Direction.POP),
                        ['state', idx+1]
                    )
                )
            code = code + Return(1)
            constructors = constructors + Function(
                Type.INTEGER,
                f'new_{typeName}',
                [Variable(Type.STATE, 'state')],
                content=code 
            )
        return constructors
    
    def declareSetters(self) -> Sequence:
        setters = Sequence()
        for typeName, definition in self.structsInfo.items():
            for field in definition.fields:
                code = Sequence()
                code = code + Struct(
                    typeName, 
                    'target', 
                    pointer=True,
                    value=Casting(
                        f'struct {typeName} *',
                        FunctionCall('lua_touserdata', ['state', 1])
                    )
                )
                code = code + StructAssign(
                    'target',
                    field.name,
                    value=FunctionCall(
                        stackPushPop(field.type_, Direction.POP),
                        ['state', 2]
                    )
                )
                code = code + Return(0)
                setters = setters + Function(
                    Type.INTEGER, 
                    f'set_{typeName}_{field.name}',
                    [Variable(Type.STATE, 'state')],
                    content=code 
                )
        return setters
    
    def declareGetters(self) -> Sequence:
        getters = Sequence()
        for typeName, definition in self.structsInfo.items():
            for field in definition.fields:
                code = Sequence()
                code = code + Struct(
                    typeName, 
                    'target', 
                    pointer=True,
                    value=Casting(
                        f'struct {typeName} *',
                        FunctionCall('lua_touserdata', ['state', 1])
                    )
                )
                code = code + Variable(
                    field.type_,
                    'result',
                    value=StructAccess('target', field.name)
                )
                code = code + FunctionCall(
                    stackPushPop(field.type_, Direction.PUSH),
                    ['state', 'result']
                )
                code = code + Return(1)
                getters = getters + Function(
                    Type.INTEGER, 
                    f'get_{typeName}_{field.name}',
                    [Variable(Type.STATE, 'state')],
                    content=code 
                )
        return getters
    
    def declareStructs(self) -> Sequence:
        container = StructDefinition(
            'container',
            [Variable(Type.STATE, 'state'), Variable(Type.INTEGER, 'registry_key')]
        )
        seq = Sequence(container)
        for struct in self.structsInfo.values():
            seq = seq + struct 
        return seq