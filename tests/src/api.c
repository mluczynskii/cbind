#include "api.h"

int increment(int n) { return n + 1; }
char foo(number_t k, char c) { return c + k; }
int sum(pair_t pair) { return pair.second + pair.first; }
char unpack(struct container cont) { return cont.character; }
struct container pack(char character) { return (struct container){character}; }
int call(int (*fptr)(int, int)) { return (*fptr)(4, 2); }