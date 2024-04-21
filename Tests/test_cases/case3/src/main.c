#include "lua_binding_api.h"

char foo(){
    return 'a';
}

int main(int argc, char** argv) {
    char *file_name = argv[1];
    
    initLua("CFunction");
    execScript(file_name);
    closeLua();

    return 0;
}