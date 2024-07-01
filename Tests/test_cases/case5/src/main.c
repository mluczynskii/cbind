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

    void* state = initLua("CFunction");
    printf("%s", execScript(state, file_name));
    closeLua(state);

    return 0;
}