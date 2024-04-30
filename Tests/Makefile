# Path to Lua source files
LUAPATH = ../lua-5.4.6

all: binding.o main

binding.o: binding.c
	gcc -c -o binding.o binding.c -L$(LUAPATH)/src -llua -lm -ldl

main: main.c binding.o
	gcc -o main main.c binding.o -L$(LUAPATH)/src -llua -lm -ldl
