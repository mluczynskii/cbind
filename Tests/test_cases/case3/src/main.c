#include <stdio.h>
#include "lua_binding_api.h"

int apply(int a,  int (*f)(int)){
    void *args[2] = {&a, f};
    return f(a);
}

int execute(int (*f)()){
    return f();
}

int inc_and_apply(int a,  int (*f)(int)){
    void *args[2] = {&a, f};
    a++;
    return f(a);
}

int foo(){
    return 42;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}