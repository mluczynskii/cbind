#include <stdio.h>
#include <stdlib.h>
#include "binding.h"

int main(int argc, char *argv[]) {
  const char *file = argv[1];
  void *state = init_lua("API");
  int status = exec_script(state, file);
  close_lua(state);
  if (status != 0)
    exit(EXIT_FAILURE);
  exit(EXIT_SUCCESS);
}