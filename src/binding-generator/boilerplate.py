code = """
lua_State* L;
pthread_mutex_t mut = PTHREAD_MUTEX_INITIALIZER;

char* execScript(const char* filename) {
pthread_mutex_lock(&mut);
if (!L) return 1;
int status = luaL_dofile(L, filename);
char* result = lua_tostring(L, -1);
pthread_mutex_unlock(&mut);
return result;
}

char* execScriptLocal(const char* filename, const char* modulename) {
lua_State* local_L = luaL_newstate();
luaL_openlibs(local_L);
lua_newtable(local_L);
luaL_setfuncs(L, &luareg, 0);
lua_setglobal(L, modulename);
int status = luaL_dofile(L, filename);
char* result = lua_tostring(L, -1);
return result;
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