#include "api.h"

int increment(int n) { return n + 1; }
char foo(number_t k, char c) { return c + k; }
//int sum(pair_t pair) { return pair.second + pair.first; }
//char unpack(struct container cont) { return cont.character; }
//struct container pack(char character) { return (struct container){character}; }
//int call(int (*fptr)(int, int)) { return (*fptr)(4, 2); }
double simple_num(short a, int b, long c, float d) { return a + b + c + d; }
//int compose(int (*f)(int), int (*g)(int, int), int x) { return (*f)((*g)(x, x)); }
//void modify(long *ptr) { *ptr = 42; }