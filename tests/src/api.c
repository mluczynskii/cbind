#include "api.h"

int increment(int n) { return n + 1; }
char foo(number_t k, char c) { return c + k; }
double simple_num(short a, int b, long c, float d) { return a + b + c + d; }
double invert_sqrt(double x) {
  return x;
}

char unpack(struct container c) { return c.character; }
int sum(pair_t pair) { return pair.second + pair.first; }

char call(char (*f)(int, char), int x, char c) { return (*f)(x, c); }
char call_typedef(function_t f, int x, char c) { return (*f)(x, c); }
int call_2(int (*f)(int), int n) { return (*f)(n); }

player_t move_player(player_t player, pair_t offset) {
  player.position.first += offset.first;
  player.position.second += offset.second;
  return player;
}

player_t take_damage(player_t player, int damage) {
  player.health = damage > player.health ? 0 : player.health - damage;
  return player;
}

static int test = 420;

void funny(int *ptr) { *ptr = 2137; }
int dereference(int *ptr) { return *ptr; }
int *grab_ptr() { return &test; }

char color_char(RGB cl) {
  switch (cl) {
    case (RED): return 'R';
    case (GREEN): return 'G';
    case (BLUE): return 'B';
  }
}

int is_black(enum CMYK cl) {
  switch (cl) {
    case (BLACK): return 1;
    default: return 0;
  }
}

RGB char_color(char c) {
  switch (c) {
    case 'R': return RED;
    case 'G': return GREEN;
    default: return BLUE;
  }
}

RGB werewolf_data(monster_t mon) {
  return mon.fur_color;
}

int vampire_data(monster_t mon) {
  return mon.years_lived;
}
