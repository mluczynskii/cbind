from abc import ABC
from dataclasses import dataclass
from typing import Self

class LuaComponent(ABC):
    pass 

class LuaSequence():
    def __init__(self, *args: LuaComponent) -> None:
        self.content = args

    def __str__(self) -> str:
        xs = map(str, self.content)
        return '\n'.join(xs)
    
    def __add__(self, xs: Self | LuaComponent) -> Self:
        if isinstance(xs, LuaSequence):
            return LuaSequence(*self.content, *xs.content)
        return LuaSequence(*self.content, xs) 

@dataclass 
class LuaFunction(LuaComponent):
    name: str 
    arglist: list[str]
    code: LuaSequence

    def __str__(self) -> str:
        arglist = ', '.join(self.arglist)
        decl = f'function {self.name} ({arglist})'
        return f'{decl}\n{self.code}\nend'
    
@dataclass 
class LuaCopyStruct(LuaComponent):
    source: str 
    target: str 

    def __str__(self) -> str:
        loop = f'for k,v in pairs({self.target}) do'
        copy = f'{self.target}[k] = {self.source}[k]'
        return f'{loop}\n{copy}\nend'
    
@dataclass 
class LuaCallApi(LuaComponent):
    modulename: str 
    functionName: str 
    arglist: list[str]
    referenceIndex: list[int]

    def __str__(self) -> str:
        arglist = ', '.join(self.arglist)
        call = f'{self.modulename}.{self.f_name}({arglist})'
        newStructs = ', '.join([f'narg{i}' for i in referenceIndex])
        return f'value, {newStructs} = {call}'
    
@dataclass 
class LuaReturn(LuaComponent):
    value: any 

    def __str__(self) -> str:
        return f'return {self.value}'
