#ifndef API
#define API

typedef struct {
  short red, green, blue;
  short alpha;
} color_t;

color_t get_default_color();
void set_attack_color(color_t *color);
void set_attack_pattern(int (*pattern)(int, int));
int get_grid_size();
int get_posx();
int get_posy();

#endif 