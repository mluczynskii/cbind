#include <stdio.h>
#include <string.h>
#include "lua_binding_api.h"

char* identity(char* a){
    return a;
}

char* min_string(char* a, char* b){
    if (strcmp(a, b) < 0) {
        return a;
    }else{
        return b;
    }
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    printf("%s", execScript(file_name));
    closeLua();

    return 0;
}