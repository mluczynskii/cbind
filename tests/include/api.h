#ifndef API
#define API

typedef struct {
  int first, second;
} pair_t;

struct container {
  char character;
};

typedef int number_t;

int increment(int n);
char foo(number_t k, char c);
double simple_num(short a, int b, long c, float d);
double invert_sqrt(double x);

int sum(pair_t pair);

typedef char (*function_t)(int, char);

char call(char (*f)(int, char), int x, char c);
char call_typedef(function_t f, int x, char c);

int call_2(int (*f)(int), int n);

#endif