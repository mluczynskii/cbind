#include <stdio.h>
#include <string.h>
#include "lua_binding_api.h"

double my_div(double a, double b){
    return a/b;
}

double my_mult(double a, double b){
    return a*b;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}