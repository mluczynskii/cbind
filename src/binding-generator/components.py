from abc import ABC
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Modifier(Enum):
    EXTERN='extern'

class Component(ABC):
    pass

@dataclass 
class Include(Component):
    name: str 
    system: Optional[bool] = False

    def __str__(self):
        if not self.system:
            return f'#include "{self.name}"'
        else:
            return f'#include <{self.name}>'

@dataclass 
class Block(Component):
    content: list[Component]

    def __str__(self):
        xs = map(str, self.content)
        inside = '\n'.join(xs)
        return '{\n' + inside + '\n}'

    def __add__(self, x):
        if not isinstance(x, Block):
            x = Block([x])
        return Block(self.content + x.content)

@dataclass
class LuaRegister(Component):
    name: str 
    f_names: list[str]

    def __str__(self):
        declaration = f'const struct luaL_Reg {self.name}[]'
        xs = ['{' + f'"{f_name}", c_{f_name}' + '}' for f_name in self.f_names]
        return declaration + ' = {\n' + ',\n'.join(xs) + '\n};'

@dataclass
class Variable(Component):
    type_: str
    name: str
    array: Optional[bool] = False
    value: Optional[any] = None

    def __str__(self):
        declaration = f'{self.type_} {self.name}'
        if self.array:
            declaration = declaration + '[]'
        return declaration + (f' = {self.value};' if self.value else ';')

@dataclass
class Function(Component):
    type_: str 
    name: str 
    args: list[str]
    modifier: Optional[any] = None
    content: Optional[Block] = None

    def __str__(self):
        mod = f'{self.modifier.value} ' if self.modifier else ''
        declaration = mod + f'{self.type_} {self.name}({", ".join(self.args)})'
        if self.content:
            return f'{declaration} {self.content}'
        else:
            return f'{declaration};'

@dataclass
class FunctionCall(Component):
    name: str
    args: list[any]
    semicolon: Optional[bool] = False

    def __str__(self):
        xs = map(str, self.args)
        return f'{self.name}({", ".join(xs)})' + (';' if self.semicolon else '')

@dataclass
class Return(Component):
    value: any 

    def __str__(self):
        return f'return {self.value};'

@dataclass 
class ContextChange(Component):
    idx: int 

    def __str__(self):
        return f'c.stack = L; c.idx = {self.idx};'

@dataclass 
class FunctionPointer(Component):
    type_: str 
    name: str 
    args: list[str]

    def __str__(self):
        xs = ', '.join(self.args)
        return f'{self.type_} (*{self.name})({xs})'

@dataclass 
class Struct(Component):
    name: str 
    fields: list[Variable]

    def __str__(self):
        prefix = f'struct {self.name}'
        content = '\n'.join(map(str, self.fields))
        return prefix + '{\n' + content + '\n};'

@dataclass 
class Context(Struct):
    pass
