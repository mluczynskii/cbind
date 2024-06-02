# Path to Lua source files
LUAPATH = ../lua-5.4.6

all: functions.o binding.o main

functions.o: functions.c
	gcc -c -o functions.o functions.c

binding.o: binding.c
	gcc -c -o binding.o binding.c -I$(LUAPATH)/src -L$(LUAPATH)/src -llua -lm -ldl

main: main.c binding.o
	gcc -o main main.c binding.o functions.o -I$(LUAPATH)/src -L$(LUAPATH)/src -llua -lm -ldl
