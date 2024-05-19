from lib.components import *

class StructHandler():
    structsInfo: dict 

    def __init__(self, data: dict) -> None:
        self.structsInfo = {}
        for f in data:
            for arg in f['args']:
                if arg['type'] not in ['struct', 'structptr_type'] :
                    continue
                fields = [Variable(x['type_name'], x['name']) for x in arg['fields']]
                struct = Struct(arg['type_name'], fields)
                self.structsInfo[arg['type_name']] = struct  

    def packStruct(self, structName: str, stackIdx: int) -> Sequence:
        seq = Sequence()
        seq = seq + FunctionCall("lua_newtable", ["L"], semicolon=True)
        struct = self.structsInfo[structName]
        for field in struct.fields:
            fieldName = field.name
            pushField = FunctionCall(
                "lua_pushinteger",
                ["L", f'arg{stackIdx}.{fieldName}'],
                semicolon=True
            )
            setField = FunctionCall(
                "lua_setfield",
                ["L", -2, f'"{fieldName}"'],
                semicolon=True
            )
            seq = seq + pushField + setField
        return seq
    
    def unpackStruct(self, structName: str, stackIdx: int) -> Sequence:
        seq = Sequence()
        struct = self.structsInfo[structName]
        for field in struct.fields:
            name = field.name
            type_ = field.type_
            pushField = FunctionCall(
                'lua_getfield',
                ['L', stackIdx, f'"{name}"'],
                semicolon=True 
            )
            saveField = Variable(
                type_,
                name,
                value=FunctionCall("lua_tonumber", ["L", -1])
            )
            seq = seq + pushField + saveField
        fieldNames = [field.name for field in struct.fields]
        return seq + InitStruct(structName, f'arg{stackIdx}', fieldNames)
    
    def declareStructs(self) -> Sequence:
        seq = Sequence()
        for struct in self.structsInfo.values():
            seq = seq + struct 
        return seq