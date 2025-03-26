/* start of boilerplate code */
#include <lua.h>
#include <lualib.h> 
#include <lauxlib.h>
#include <callback.h> 
#include <stdlib.h>
#include <stdio.h>
#include "api.h"

extern const luaL_Reg functions[];

void* init_lua(const char* modulename) {
    lua_State *state = luaL_newstate();
    luaL_openlibs(state);
    lua_newtable(state);
    luaL_setfuncs(state, functions, 0);
    lua_setglobal(state, modulename);
    return (void*)state;
}

int exec_script(void* state, const char* filename) {
  lua_State *L = (lua_State *)state;
  int status = luaL_dofile(L, filename);
  if (status != 0)
    fprintf(stderr, "%s\n", lua_tostring(L, -1));
  return status;
}

void close_lua(void* state) {
  lua_close((lua_State *)state);
}

/* end of boilerplate code */
/* start of auto-generated code */
