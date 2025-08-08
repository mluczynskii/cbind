compile:
	gcc -c -fdump-tree-original-raw -o api.o api.c 
	python3 ../cbind/parser.py api.c.006t.original
	python3 ../cbind/main.py dump.json --filter filter 
	gcc -c binding.c -o binding.o
	gcc -c main.c -o main.o 
	gcc -o main main.o api.o binding.o -llua -lffcall -lm -lSDL2

clean:
	rm *.o *.original *.json main binding.c binding.h