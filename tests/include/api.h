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
int sum(pair_t pair);
char unpack(struct container cont);

#endif