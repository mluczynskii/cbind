#include "lua_binding_api.h"

int apply(int a,  int (*f)(int)){
    return f(a);
}

int execute(int (*f)()){
    return f();
}

int inc_and_apply(int a,  int (*f)(int)){
    a++;
    return f(a);
}

int foo(){
    return 42;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    execScript(file_name);
    closeLua();

    return 0;
}