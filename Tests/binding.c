#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>
#include <callback.h>
#include <stdlib.h>

void* callbackStorage[20];
void* dataStorage[20];
int storageIdx = 0;

struct container{
lua_State* state;
int registry_key;
};
struct Counter{
int val;
};

int new_Counter(lua_State* state) {
size_t nbytes = sizeof(struct Counter);
struct Counter* result = (struct Counter *)(lua_newuserdata(state, nbytes));
result->val = lua_tointeger(state, 1);
return 1;
};

int set_Counter_val(lua_State* state) {
struct Counter* target = (struct Counter *)(lua_touserdata(state, 1));
target->val = lua_tointeger(state, 2);
return 0;
};

int get_Counter_val(lua_State* state) {
struct Counter* target = (struct Counter *)(lua_touserdata(state, 1));
int result = target->val;
lua_pushinteger(state, result);
return 1;
};

extern void increment(struct Counter* cnt);
extern void decrement(struct Counter* cnt);



int c_increment(lua_State* state) {
struct Counter* cnt = (struct Counter *)(lua_touserdata(state, 1));
increment(cnt);
return 0;
};
int c_decrement(lua_State* state) {
struct Counter* cnt = (struct Counter *)(lua_touserdata(state, 1));
decrement(cnt);
return 0;
};

const struct luaL_Reg luareg[] = {
{ "increment", c_increment },
{ "decrement", c_decrement }
};

const struct luaL_Reg counterlib[] = {
    {"new", new_Counter},
    {"set", set_Counter_val},
    {"get", get_Counter_val}
};

void* initLua(const char* modulename) {
    lua_State* state = luaL_newstate();
    luaL_openlibs(state);
    lua_newtable(state);
    luaL_setfuncs(state, &luareg, 0);
    lua_setglobal(state, modulename);
    luaL_openlib(state, "Counter", counterlib, 0);
    return (void*)state;
}

char* execScript(void* state, const char* filename) {
    lua_State* L = (lua_State*)state;
    int status = luaL_dofile(L, filename);
    char* result = lua_tostring(L, -1);
    return result;
}

void closeLua(void* state) {
    for (int idx = 0; idx < storageIdx; idx++) {
        if (callbackStorage[idx] != 0) {
            free_callback(callbackStorage[idx]);
            free(dataStorage[idx]);
        }
    }
    storageIdx = 0;
    lua_close((lua_State*)state);
}


