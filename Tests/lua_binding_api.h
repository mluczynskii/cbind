#ifndef LUA_API_H
#define LUA_API_H

void initLua(const char* modulename);
int execScript(const char* filename);
void closeLua();

#endif
