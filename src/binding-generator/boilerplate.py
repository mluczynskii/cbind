code = """

void* initLua(const char* modulename) {
    lua_State* state = luaL_newstate();
    luaL_openlibs(state);
    lua_newtable(state);
    luaL_setfuncs(state, &luareg, 0);
    lua_setglobal(state, modulename);
    return (void*)state;
}

char* execScript(void* state, const char* filename) {
    lua_State* L = (lua_State*)state;
    int status = luaL_dofile(L, filename);
    char* result = lua_tostring(L, -1);
    return result;
}

void closeLua(void* state) {
    lua_close((lua_State*)state);
}

"""