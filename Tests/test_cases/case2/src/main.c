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
    
    initLua("CFunction");
    printf("%s", execScript(file_name));
    closeLua();

    return 0;
}