#include <stdio.h>
#include <unistd.h>
#include <pthread.h> 
#include <stdbool.h>
#include "lua_binding_api.h"

#define buff_size 5

pthread_mutex_t lock;
bool running = true;
void* state;

int (*functions[buff_size])();

void add_function(int (*f)(), int i){
    pthread_mutex_lock(&lock);
    functions[i] = f;
    pthread_mutex_unlock(&lock);
}

void delete_function(int i){
    pthread_mutex_lock(&lock);
    functions[i] = NULL;
    pthread_mutex_unlock(&lock);
}

void* call_functions(void* arg){
    while(running){
        sleep(1);
        pthread_mutex_lock(&lock);
        for(int i = 0; i < buff_size; i++){
            if(functions[i] != NULL){
                functions[i]();
            }
        }
        pthread_mutex_unlock(&lock);
    }

    return NULL;
}

void* event_listener(void* arg) {
    char *file_name = (char *)arg;

    printf("%s", execScript(state, file_name));

    running = false;

    return NULL;
}

int main(int argc, char** argv){
    char *file_name = argv[1];
    pthread_t thread1, thread2;

    state = initLua("CFunction");

    if (pthread_mutex_init(&lock, NULL) != 0) {
        printf("Mutex initialization error\n");
        return 1;
    }

    pthread_create(&thread1, NULL, call_functions, NULL);
    pthread_create(&thread2, NULL, event_listener, file_name);

    pthread_join(thread2, NULL);

    pthread_join(thread1, NULL);

    pthread_mutex_destroy(&lock);

    closeLua(state);
}