#include <stdio.h>
#include <string.h>
#include "lua_binding_api.h"

float my_div(float a, float b){
    return a/b;
}

float my_mult(float a, float b){
    return a*b;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}