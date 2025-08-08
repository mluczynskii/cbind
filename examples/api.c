#include "api.h"

extern color_t *attack_color;
extern int (*attack_pattern)(int, int);
extern const int GRID_SIZE;
extern int posx, posy;

void set_attack_color(color_t *color) { attack_color = color; }
void set_attack_pattern(int (*pattern)(int, int)) { attack_pattern = pattern; }
int get_grid_size() { return GRID_SIZE; }
color_t get_default_color() {
  color_t def = {
    .red = 255, .green = 0, .blue = 0,
    .alpha = 255
  };
  return def;
}
int get_posx() { return posx; }
int get_posy() { return posy; }