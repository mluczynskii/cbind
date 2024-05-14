#include <stdio.h>
#include "lua_binding_api.h"

struct Counter{
    int val;
};

void increment(struct Counter *cnt){
    cnt->val++;
}

void decrement(struct Counter *cnt){
    cnt->val--;
}

int main(int argc, char** argv) {
    char *file_name = argv[1];

    initLua("CFunction");
    printf("%s", execScript(file_name));
    closeLua();

    return 0;
}