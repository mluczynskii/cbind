#include <SDL2/SDL.h>
#include <stdlib.h>
#include <time.h>
#include "binding.h"
#include "api.h"

const int GRID_SIZE = 5, CELL_SIZE = 200, WINDOW_SIZE = GRID_SIZE * CELL_SIZE;
const int ATTACK_LIFETIME = 1000;
color_t *attack_color = NULL;
int (*attack_pattern)(int, int) = NULL;
int posx = GRID_SIZE / 2, posy = GRID_SIZE / 2;

typedef struct {
  SDL_Rect rect;
  Uint32 timestamp;
  int active;
} SDL_TimedRect;

static int max (int a, int b) { return (a > b) ? a : b; }
static int min (int a, int b) { return (a > b) ? b : a; }

int main() {
  SDL_Init(SDL_INIT_VIDEO);
  SDL_Window* window = SDL_CreateWindow("Robo-bitch",
      SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
      WINDOW_SIZE, WINDOW_SIZE, 0
  );
  SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

  int running = 1;
  SDL_Event event;

  SDL_TimedRect attacks[GRID_SIZE][GRID_SIZE];

  void *state = cbind_init("API");

  while (running) {
    Uint32 now = SDL_GetTicks();

    while (SDL_PollEvent(&event)) {
      if (event.type == SDL_QUIT) 
        running = 0;
      if (event.type == SDL_KEYDOWN) {
        SDL_Keycode keycode = event.key.keysym.sym;
        if (keycode == SDLK_LEFT) posx = max(posx - 1, 0);
        else if (keycode == SDLK_RIGHT) posx = min(posx + 1, GRID_SIZE-1);
        else if (keycode == SDLK_UP) posy = max(posy - 1, 0);
        else if (keycode == SDLK_DOWN) posy = min(posy + 1, GRID_SIZE-1);
        else if (keycode == SDLK_r) 
          (void)cbind_execute(state, "script.lua");
        if (keycode == SDLK_SPACE) {
          if (attack_pattern != NULL) {
            for (int x = 0; x < GRID_SIZE; x++) {
              for (int y = 0; y < GRID_SIZE; y++) {
                if ((*attack_pattern)(x, y)) {
                  SDL_Rect attack_cell = {
                    x * CELL_SIZE + 10, y * CELL_SIZE + 10,
                    CELL_SIZE - 20, CELL_SIZE - 20
                  };
                  attacks[y][x].rect = attack_cell;
                  attacks[y][x].timestamp = now;
                  attacks[y][x].active = 1;
                }
              }
            }
          }
        }
      }
    }

    SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255); 
    SDL_RenderClear(renderer);
        
    SDL_SetRenderDrawColor(renderer, 200, 200, 200, 255);
    for (int i = 0; i <= GRID_SIZE; i++) {
      SDL_RenderDrawLine(renderer, i * CELL_SIZE, 0, i * CELL_SIZE, WINDOW_SIZE);
      SDL_RenderDrawLine(renderer, 0, i * CELL_SIZE, WINDOW_SIZE, i * CELL_SIZE);
    }

    if (attack_color != NULL) {
      SDL_SetRenderDrawColor(
        renderer, 
        attack_color->red, attack_color->green, attack_color->blue,
        attack_color->alpha
      );
      for (int x = 0; x < GRID_SIZE; x++) {
        for (int y = 0; y < GRID_SIZE; y++) {
          if (attacks[y][x].active && now - attacks[y][x].timestamp < ATTACK_LIFETIME)
            SDL_RenderFillRect(renderer, &attacks[y][x].rect);
          else 
            attacks[y][x].active = 0;
        }
      }
    }

    SDL_Rect robot = {
      posx * CELL_SIZE + 10,
      posy * CELL_SIZE + 10,
      CELL_SIZE - 20,
      CELL_SIZE - 20
    };
    SDL_SetRenderDrawColor(renderer, 0, 255, 0, 255);
    SDL_RenderFillRect(renderer, &robot);

    SDL_RenderPresent(renderer);
    SDL_Delay(16);
  }

  cbind_close(state);
  SDL_DestroyRenderer(renderer);
  SDL_DestroyWindow(window);
  SDL_Quit();
  return 0;
}
