#include <stdio.h>
#include <string.h>
#include "lua_binding_api.h"

double div(double a, double b){
    return a/b;
}

double mult(double a, double b){
    return a*b;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    printf("%s", execScript(file_name));
    closeLua();

    return 0;
}