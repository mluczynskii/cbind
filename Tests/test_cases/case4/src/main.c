#include "lua_binding_api.h"
#include <string.h>

typedef struct {
    int x, y;
} Fraction;

int numerator(Fraction a){
    return a.x;
}

typedef struct {
    char* val;
} String;

int string_compare(String a, String b){
    return strcmp(a.val, b.val);
}

typedef struct {
    int val;
} Int;

int multiply(Int a, int b){
    return a.val * b;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    execScript(file_name);
    closeLua();

    return 0;
}