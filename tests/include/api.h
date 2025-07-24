#ifndef API
#define API

typedef struct {
  int first, second;
} pair_t;

struct container {
  char character;
};

typedef struct {
  pair_t position;
  int health;
} player_t;

typedef int number_t;

int increment(int n);
char foo(number_t k, char c);
double simple_num(short a, int b, long c, float d);
double invert_sqrt(double x);

int sum(pair_t pair);
char unpack(struct container c);

typedef char (*function_t)(int, char);

char call(char (*f)(int, char), int x, char c);
char call_typedef(function_t f, int x, char c);
int call_2(int (*f)(int), int n);

player_t move_player(player_t player, pair_t offset);
player_t take_damage(player_t player, int damage);

void funny(int *ptr);
int dereference(int *ptr);
int *grab_ptr();

typedef enum {
  RED, GREEN, BLUE
} RGB;

enum CMYK {
  CYAN, MAGENTA = 10, YELLOW, BLACK
};

char color_char(RGB cl);
int is_black(enum CMYK cl);
RGB char_color(char c);

#endif