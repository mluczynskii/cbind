#include "../include/api.h"
#include <stdio.h>

int increment(int n) { return n + 1; }
char foo(number_t k, char c) { return c + k; }
double simple_num(short a, int b, long c, float d) { return a + b + c + d; }
double invert_sqrt(double x) {
  return x;
}

int sum(pair_t pair) { return pair.second + pair.first; }
//char unpack(struct container cont) { return cont.character; }
//struct container pack(char character) { return (struct container){character}; }
