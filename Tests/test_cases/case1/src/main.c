#include <stdio.h>
#include "lua_binding_api.h"

int inc(int a){
    return a + 1;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}