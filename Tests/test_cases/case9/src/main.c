#include <stdio.h>
#include <string.h>
#include "lua_binding_api.h"

long inc(long x){
    return x+1;
}

long square(long x){
    return x*x;
}

long int add(long int x, long int y){
    return x+y;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    printf("%s", execScript(file_name));
    closeLua();

    return 0;
}