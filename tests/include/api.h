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
//int sum(pair_t pair);
//char unpack(struct container cont);
//struct container pack(char character);
//int call(int (*fptr)(int, int));
double simple_num(short a, int b, long c, float d);
//int compose(int (*f)(int), int (*g)(int, int), int x);
//void modify(long *ptr);

#endif