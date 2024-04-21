#include "lua_binding_api.h"

int inc(int a){
    return a + 1;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    execScript(file_name);
    closeLua();

    return 0;
}