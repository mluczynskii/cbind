#include <stdio.h>
#include <string.h>
#include "lua_binding_api.h"

short inc(short x){
    return x+1;
}

short square(short x){
    return x*x;
}

short int add(short int x, short int y){
    return x+y;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}