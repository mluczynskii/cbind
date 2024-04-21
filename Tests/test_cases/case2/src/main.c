#include "lua_binding_api.h"

int bar(){
    return 10;
}

int foo(int x){
    return x*x;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];
    
    initLua("CFunction");
    execScript(file_name);
    closeLua();

    return 0;
}