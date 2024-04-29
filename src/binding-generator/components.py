from abc import ABC
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Modifier(Enum):
    CONST = 'const'
    EXTERN = 'extern'

class Component(ABC):
    pass

# Include directive, ex. #include <stdio.h>
@dataclass 
class Include(Component):
    name: str 
    system: Optional[bool] = False

    def __str__(self):
        if not self.system:
            return f'#include "{self.name}"';
        else:
            return f'#include <{self.name}>';

# Code block, ex. { int x = 5; return x; }
@dataclass 
class Block(Component):
    content: list[Component]

    def __str__(self):
        xs = map(str, self.content);
        inside = '\n'.join(xs);
        return '{\n' + inside + '\n}';

    def __add__(self, x):
        if not isinstance(x, Block):
            x = Block([x]);
        return Block(self.content + x.content);

@dataclass
class LuaRegister(Component):
    name: str 
    values: list[str]

    def __str__(self):
        declaration = f'const struct luaL_Reg {self.name}[]';
        inside = ',\n'.join(self.values);
        return declaration + ' = {\n' + inside + '\n};';

# Variable declaration, ex. int x = 5;
@dataclass
class Variable(Component):
    type_: str
    name: str
    array: Optional[bool] = False
    modifier: Optional[Modifier] = None
    value: Optional[any] = None

    def __str__(self):
        mod = f'{self.modifier.value} ' if self.modifier else '';
        declaration = mod + f'{self.type_} {self.name}';
        if self.array:
            declaration = declaration + '[]';
        return declaration + (f' = {self.value};' if self.value else ';');

# Function declaration, ex. int foo(int n) { return n+1; }
@dataclass
class Function(Component):
    type_: str 
    name: str 
    args: list[str]
    modifier: Optional[Modifier] = None
    content: Optional[Block] = None

    def __str__(self):
        mod = f'{self.modifier.value} ' if self.modifier else '';
        declaration = mod + f'{self.type_} {self.name}({", ".join(self.args)})';
        if self.content:
            return f'{declaration} {self.content}';
        else:
            return f'{declaration};';

@dataclass
class FunctionCall(Component):
    name: str
    args: list[any]
    semicolon: Optional[bool] = False

    def __str__(self):
        xs = map(str, self.args);
        return f'{self.name}({", ".join(xs)})' + (';' if self.semicolon else '');

@dataclass
class Return(Component):
    value: any 

    def __str__(self):
        return f'return {self.value};';

# struct declaration, ex. struct context { int idx; char c; };
@dataclass 
class Struct(Component):
    name: str 
    fields: list[Variable]

    def __str__(self):
        prefix = f'struct {self.name} ';
        xs = map(str, self.fields);
        content = '\n'.join(xs);
        return prefix + '{\n' + content + '\n};'

@dataclass 
class ContextChange(Component):
    idx: int 

    def __str__(self):
        return f'c.stack = L; c.idx = {self.idx};';

class Blank(Component):
    def __str__(self):
        return '';
        
@dataclass
class Sequence():
    content: list[Component]

    def __add__(self, xs: Component | list[Component]):
        if isinstance(xs, Component):
            xs = [xs];
        return Sequence(self.content + xs);

    def __str__(self):
        output = '';
        for component in self.content:
            output = str(component) + '\n';
        return output;

@dataclass 
class FunctionPointer(Component):
    return_type: str 
    name: str 
    args: list[str]

    def __str__(self):
        xs = ', '.join(self.args);
        return f'{self.return_type} (*{self.name})({xs})';