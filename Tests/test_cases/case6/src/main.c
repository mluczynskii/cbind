#include <stdio.h>
#include "lua_binding_api.h"

char identity(char a){
    return a;
}

char min_char(char a, char b) {
    return (a < b) ? a : b;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}