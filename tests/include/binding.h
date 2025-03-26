#ifndef BINDING
#define BINDING

typedef struct {
  
} closure_t;

void * init_lua(const char *module);
int exec_script(void *state, const char *file);
void close_lua(void *state);

#endif