#include <stdio.h>
#include "lua_binding_api.h"

int return_ten(){
    return 10;
}

int square(int x){
    return x*x;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];
    
    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}