#include <stdio.h>
#include "lua_binding_api.h"
#include "functions.h"

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    printf("%s", execScript(file_name));
    closeLua();

    return 0;
}