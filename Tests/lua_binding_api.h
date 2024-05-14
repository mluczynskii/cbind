#ifndef LUA_API_H
#define LUA_API_H

void initLua(const char* modulename);
char* execScript(const char* filename);
void closeLua();

#endif
