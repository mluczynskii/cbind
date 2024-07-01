#include <stdio.h>
#include "lua_binding_api.h"


int add(int x, int y){
    return x + y;
}

int sub(int x, int y){
    return x - y;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}