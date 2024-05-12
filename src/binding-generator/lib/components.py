from abc import ABC
from dataclasses import dataclass
from typing import Optional, Self
from enum import Enum

class Modifier(Enum):
    EXTERN='extern'

class Component(ABC):
    pass
 
class Sequence():
    def __init__(self, *args: Component) -> None:
        self.content = args

    def __str__(self) -> str:
        xs = map(str, self.content)
        return '\n'.join(xs)
    
    def __add__(self, xs: Self | Component) -> Self:
        if isinstance(xs, Sequence):
            return Sequence(*self.content, *xs.content)
        return Sequence(*self.content, xs) 
    
@dataclass 
class Block(Component):
    seq: Sequence

    def __str__(self) -> str:
        return '{\n' + str(self.seq) + '\n}'
    
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
    functions: list[str]

    def __str__(self) -> str:
        declaration = f'const struct luaL_Reg {self.name}[]'
        xs = [f'{{ "{f}", c_{f} }}' for f in self.functions]
        return declaration + ' = {\n' + ',\n'.join(xs) + '\n};'

@dataclass
class Variable(Component):
    type_: str
    name: str
    array: Optional[bool] = False
    value: Optional[any] = None

    def __str__(self) -> str:
        declaration = f'{self.type_} {self.name}'
        if self.array:
            declaration = declaration + '[]'
        return declaration + (f' = {self.value};' if self.value else ';')

@dataclass
class Function(Component):
    type_: str 
    name: str 
    args: list[str]
    modifier: Optional[Modifier] = None
    seq: Optional[Sequence] = None

    def __str__(self) -> str:
        mod = f'{self.modifier.value} ' if self.modifier else ''
        arglist = ', '.join(self.args)
        declaration = mod + f'{self.type_} {self.name}({arglist})'
        if self.seq:
            content = Block(self.seq)
            return f'{declaration} {content}'
        return f'{declaration};'

@dataclass
class FunctionCall(Component):
    name: str
    args: list[any]
    semicolon: Optional[bool] = False

    def __str__(self) -> str:
        xs = ', '.join(map(str, self.args))
        return f'{self.name}({xs})' + (';' if self.semicolon else '')

@dataclass
class Return(Component):
    value: any 

    def __str__(self) -> str:
        return f'return {self.value};'

@dataclass 
class ContextChange(Component):
    idx: int 

    def __str__(self) -> str:
        return f'c.stack = L; c.idx = {self.idx};'

@dataclass 
class FunctionPointer(Component):
    type_: str 
    name: str 
    args: list[str]

    def __str__(self) -> str:
        arglist = ', '.join(self.args)
        return f'{self.type_} (*{self.name})({arglist})'

@dataclass 
class Struct(Component):
    name: str 
    fields: list[Variable]

    def __str__(self) -> str:
        declaration = f'struct {self.name}'
        content = '\n'.join(map(str, self.fields))
        return declaration + '{\n' + content + '\n};'
    
@dataclass 
class InitStruct(Component):
    struct: str
    name: str 
    values: list[str]

    def __str__(self) -> str:
        values = ','.join(self.values)
        return f'struct {self.struct} {self.name} = {{ {values} }};'

