code = """
lua_State* L;

int execScript(const char* filename) {
if (!L) return 1;
int status = luaL_dofile(L, filename);
return status;
}

void initLua(const char* modulename) {
L = luaL_newstate();
luaL_openlibs(L);

lua_newtable(L);
luaL_setfuncs(L, &luareg, 0);
lua_setglobal(L, modulename);
}

void closeLua() {
lua_close(L);
}
"""