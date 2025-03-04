#include <stdio.h>
#include "api.h"

int main(int argc, char *argv[]) {
  const char *file = argv[1];
  void *state = init_lua("API");
  printf("Output of %s: %s\n", file, exec_script(state, file));
  close_lua(state);
  return 0;
}