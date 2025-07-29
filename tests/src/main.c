#include <stdio.h>
#include <stdlib.h>
#include "binding.h"

int main(int argc, char *argv[]) {
  const char *file = argv[1];
  void *state = cbind_init("API");
  int status = cbind_execute(state, file);
  cbind_close(state);
  if (status != 0)
    exit(EXIT_FAILURE);
  exit(EXIT_SUCCESS);
}