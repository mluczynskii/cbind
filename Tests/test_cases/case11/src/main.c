#include <stdio.h>
#include <string.h>
#include "lua_binding_api.h"

float div(float a, float b){
    return a/b;
}

float mult(float a, float b){
    return a*b;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    printf("%s", execScript(file_name));
    closeLua();

    return 0;
}