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

    def packStruct(self, structName: str, stackIdx: int) -> Sequence:
        pass # TODO: rewrite this shit code
    
    def unpackStruct(self, varName: str, structName: str, idx: int) -> Tuple[Sequence, Struct]:
        seq = Sequence()
        struct = self.structsInfo[structName]
        for field in struct.fields:
            name = field.name
            type_ = field.type_
            pushField = FunctionCall('lua_getfield', ['state', idx, f'"{name}"'])
            popFunction = stackPushPop(type_, Direction.POP)
            saveField = Variable(type_, name, value=FunctionCall(popFunction, ["state", -1]))
            seq = seq + pushField + saveField
        fieldNames = [field.name for field in struct.fields]
        component = Struct(structName, varName)
        seq = seq + component
        for fieldName in fieldNames:
            seq = seq + StructAssign(varName, fieldName, fieldName, pointer=False)
        return seq, component
    
    def declareStructs(self) -> Sequence:
        container = StructDefinition(
            'container',
            [Variable(Type.STATE, 'state'), Variable(Type.INTEGER, 'registry_key')]
        )
        seq = Sequence(container)
        for struct in self.structsInfo.values():
            seq = seq + struct 
        return seq