#include "../include/api.h"

int increment(int n) { return n + 1; }
char foo(number_t k, char c) { return c + k; }
double simple_num(short a, int b, long c, float d) { return a + b + c + d; }
double invert_sqrt(double x) {
  return x;
}

int sum(pair_t pair) { return pair.second + pair.first; }

char call(char (*f)(int, char), int x, char c) { return (*f)(x, c); }
char call_typedef(function_t f, int x, char c) { return (*f)(x, c); }

int call_2(int (*f)(int), int n) { return (*f)(n); }