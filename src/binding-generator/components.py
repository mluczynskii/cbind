# TODO: Fix indentation problems

from abc import ABC
from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Modifier(Enum):
    CONST = 'const'
    EXTERN = 'extern'

class Component(ABC):
    pass

class Directive(ABC):
    pass

class Statement(ABC):
    pass

# Include directive, ex. #include <stdio.h>
@dataclass 
class Include(Directive):
    name: str 
    user: bool

    def __str__(self):
        if self.user:
            return f'#include "{self.name}"';
        else:
            return f'#include <{self.name}>';

# Code block, ex. { int x = 5; return x; }
@dataclass 
class Block(Component):
    content: list[Statement]

    def __str__(self):
        xs = map(str, self.content);
        inside = '\n'.join(xs);
        return '{\n' + inside + '\n}';

    @staticmethod
    def merge(x, y):
        return Block(x.content + y.content);

@dataclass
class LuaRegister(Statement):
    name: str 
    values: list[str]

    def __str__(self):
        declaration = f'const struct luaL_Reg {self.name}[]';
        inside = ',\n'.join(self.values);
        return declaration + ' = {\n' + inside + '\n};';

# Variable declaration, ex. int x = 5;
@dataclass
class Variable(Statement):
    type_: str
    name: str
    array: bool
    modifier: Optional[Modifier] = None
    value: Optional[any] = None

    def __str__(self):
        mod = self.modifier.value + ' ' if self.modifier else '';
        declaration = mod + f'{self.type_} {self.name}';
        if self.array:
            declaration = declaration + '[]';
        return declaration + (f' = {self.value};' if self.value else ';');

# Function declaration, ex. int foo (int n);
@dataclass
class Function(Statement):
    return_type: str 
    name: str 
    args: list[str]
    modifier: Optional[Modifier] = None
    content: Optional[Block] = None

    def __str__(self):
        mod = self.modifier.value + ' ' if self.modifier else '';
        xs = map(str, self.args);
        declaration = mod + f'{self.return_type} {self.name}({", ".join(xs)})';
        if self.content:
            return f'{declaration} {self.content}';
        else:
            return f'{declaration};';

@dataclass
class FunctionCall(Statement):
    name: str
    args: list[any]
    semicolon: Optional[bool] = False

    def __str__(self):
        xs = map(str, self.args);
        return f'{self.name}({", ".join(xs)})' + (';' if self.semicolon else '');

@dataclass
class Return(Statement):
    value: any 

    def __str__(self):
        return f'return {self.value};';