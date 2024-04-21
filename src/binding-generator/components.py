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
            return f'#include "{self.name}" \n';
        else:
            return f'#include <{self.name}> \n';

# Code block, ex. { int x = 5; return x }
@dataclass 
class Block(Component):
    content: list[Statement]

    def __str__(self):
        xs = map(str, self.content);
        inside = '\n    '.join(xs);
        return '{\n    ' + inside + '}\n';

    @staticmethod
    def merge(x, y):
        return Block(x.content + y.content);

@dataclass
class ListInitializer(Component):
    values: list[str]

    def __str__(self):
        return '{\n' + ',\n'.join(self.values) +'\n};\n';

# Variable declaration, ex. int x = 5;
@dataclass
class Variable(Statement):
    struct: bool
    type_: str
    name: str
    array: bool
    modifier: Optional[Modifier] = None
    value: Optional[any] = None

    def __str__(self):
        mod = self.modifier.value + ' ' if self.modifier else '';
        prefix = mod + ('struct ' if self.struct else '');
        declaration = f'{prefix}{self.type_} {self.name}';
        if self.array:
            declaration = declaration + '[]';
        final = declaration + (f' = {self.value}' if self.value else '');
        if not (isinstance(self.value, Block) or isinstance(self.value, ListInitializer)):
            final = final + ';';
        return final;

# Function declaration, ex. int foo (int n);
@dataclass
class Function(Statement):
    return_type: str 
    name: str 
    args: list[Variable]
    modifier: Optional[Modifier] = None
    content: Optional[Block] = None

    def __str__(self):
        mod = self.modifier.value + ' ' if self.modifier else '';
        xs = map(str, self.args);
        declaration = f'{mod}{self.return_type} {self.name}({', '.join(xs)})';
        if self.content:
            return f'{declaration} {self.content} \n';
        else:
            return f'{declaration}; \n';

@dataclass
class FunctionCall(Statement):
    name: str
    args: list[any]
    last: Optional[bool] = False

    def __str__(self):
        xs = map(str, self.args);
        return f'{self.name}({', '.join(xs)})' + (';' if self.last else '');

@dataclass
class Return(Statement):
    value: any 

    def __str__(self):
        return f'return {self.value}; \n';