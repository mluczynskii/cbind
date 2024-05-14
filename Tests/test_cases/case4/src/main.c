#include <stdio.h>
#include "lua_binding_api.h"

struct Fraction{
    int x, y;
};

int numerator(struct Fraction a){
    void *args[2] = {&a.x, &a.y};
    return a.x;
}

struct Int{
    int val;
};

int multiply(struct Int a, int b){
    void *args[2] = {&a, &b};
    return a.val * b;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    printf("%s", execScript(file_name));
    closeLua();

    return 0;
}