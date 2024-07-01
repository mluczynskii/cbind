#include <stdio.h>
#include <string.h>
#include "lua_binding_api.h"

const char* identity(const char* a){
    return a;
}

const char* min_string(const char* a, const char* b){
    if (strcmp(a, b) < 0) {
        return a;
    }else{
        return b;
    }
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}