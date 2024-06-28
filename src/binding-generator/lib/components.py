from abc import ABC
from dataclasses import dataclass
from typing import Optional, Self
from enum import Enum

class Modifier(Enum):
    EXTERN='extern'

class Type(Enum):
    INTEGER='int'
    FLOAT='float'
    DOUBLE='double'
    CHAR='char'
    LONG='long'
    SHORT='short'
    STRING='char*'
    VOID='void'
    VOID_PTR='void*'
    VA_LIST='va_alist'
    STATE='lua_State*'

class Direction(Enum):
    PUSH = 'push'
    POP = 'pop'

def parseType(name: str) -> Type:
    for type_ in Type:
        if type_.value == name:
            return type_
    raise NotImplementedError(f'Unknown data type: {name}')

def stackPushPop(type_: Type, dir: Direction) -> str:
    if type_ in [Type.INTEGER, Type.SHORT, Type.LONG]:
        if dir == Direction.PUSH:
            return 'lua_pushinteger'
        return 'lua_tointeger'
    elif type_ in [Type.FLOAT, Type.DOUBLE]:
        if dir == Direction.PUSH:
            return 'lua_pushnumber'
        return 'lua_tonumber'
    elif type_ in [Type.STRING]:
        if dir == Direction.PUSH:
            return 'lua_pushstring'
        return 'lua_tostring'
    elif type_ in [Type.CHAR]:
        if dir == Direction.PUSH:
            return 'lua_pushstringl'
        return 'lua_tostring'
    raise NotImplementedError('Type not compatible with Lua')

class Component(ABC):
    pass
 
class Sequence():
    def __init__(self, *args: Component) -> None:
        self.content = args

    def __str__(self) -> str:
        xs = map(lambda s : f'{s};', self.content)
        return '\n'.join(xs)
    
    def __add__(self, xs: Self | Component) -> Self:
        if isinstance(xs, Sequence):
            return Sequence(*self.content, *xs.content)
        return Sequence(*self.content, xs) 
    
@dataclass 
class Block(Component):
    content: Sequence

    def __str__(self) -> str:
        return '{\n' + str(self.content) + '\n}'
    
@dataclass 
class Include(Component):
    name: str 
    system: Optional[bool] = False

    def __str__(self) -> str:
        if not self.system:
            return f'#include "{self.name}"'
        return f'#include <{self.name}>'

@dataclass
class LuaRegister(Component):
    name: str 
    functions: dict

    def __str__(self) -> str:
        declaration = f'const struct luaL_Reg {self.name}[]'
        xs = []
        for apiName, wrapperName in self.functions.items():
            xs.append(f'{{ "{apiName}", {wrapperName} }}')
        return declaration + ' = {\n' + ',\n'.join(xs) + '\n};'

@dataclass
class Variable(Component):
    type_: Type
    name: str
    array: Optional[bool] = False
    value: Optional[any] = None

    def __str__(self) -> str:
        var = f'{self.type_.value} {self.name}'
        if self.array:
            var = var + '[]'
        if self.value:
            var = var + f' = {self.value}'
        return var
    
@dataclass 
class Struct(Component):
    structName: str 
    variableName: str 
    pointer: Optional[bool] = False 
    array: Optional[bool] = False 
    value: Optional[any] = None 

    def __str__(self) -> str:
        var = f'struct {self.structName}'
        if self.pointer:
            var = var + '*'
        var = f'{var} {self.variableName}'
        if self.array:
            var = var + '[]'
        if self.value:
            var = f'{var} = {self.value}'
        return var
    
@dataclass 
class FunctionPointer(Component):
    returnType: Type  
    name: str 
    args: list[Type]

    def __str__(self) -> str:
        arglist = map(lambda s : s.value, self.args)
        arglist = ', '.join(arglist)
        return f'{self.returnType} (*{self.name})({arglist})'

@dataclass
class Function(Component):
    returnType: Type
    name: str 
    args: list[Variable | FunctionPointer]
    modifier: Optional[Modifier] = None
    content: Optional[Sequence] = None

    def __str__(self) -> str:
        mod = f'{self.modifier.value} ' if self.modifier else ''
        arglist = ', '.join(map(str, self.args))
        func = mod + f'{self.returnType.value} {self.name}({arglist})'
        if self.content:
            content = Block(self.content)
            func = f'{func} {content}'
        return func 

@dataclass
class FunctionCall(Component):
    name: str
    args: list[any]

    def __str__(self) -> str:
        xs = ', '.join(map(str, self.args))
        return f'{self.name}({xs})'

@dataclass
class Return(Component):
    value: any 

    def __str__(self) -> str:
        return f'return {self.value}'

@dataclass 
class StructDefinition(Component):
    name: str 
    fields: list[Variable]

    def __str__(self) -> str:
        declaration = f'struct {self.name}'
        content = Sequence(*self.fields)
        return declaration + '{\n' + str(content) + '\n}'
    
@dataclass 
class Closure(Component):
    functionType: FunctionPointer
    prototypeName: str # name of the prototype function
    containerName: str # data pointer passed to the closure
    
    def __str__(self) -> str:
        alloc = FunctionCall(
            'alloc_callback', 
            [f'&{self.prototypeName}', self.containerName]
        )
        return f'{self.functionType} = {alloc}'
    
@dataclass 
class StructAccess(Component):
    varName: str 
    fieldName: str 
    pointer: Optional[bool] = True 
    
    def __str__(self) -> str:
        join = '->' if self.pointer else '.'
        return f'{self.varName}{join}{self.fieldName}'
    
@dataclass 
class StructAssign(StructAccess):
    value: any 

    def __str__(self) -> str:
        var = super.__str__()
        return f'{var} = {self.value}'
    
@dataclass 
class Casting(Component):
    castType: Type | str 
    value: any 

    def __str__(self) -> str:
        type_ = self.castType 
        if isinstance(self.castType, Type):
            type_ = self.castType.value 
        return f'({type_})({self.value})'
