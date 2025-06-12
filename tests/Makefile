IDIR=./include
SDIR=./src

LIBS=-lm -llua

_DEPS = api.h binding.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

OBJ = api.o binding.o main.o

CFLAGS=-I$(IDIR) -I/usr/local/include -L/usr/local/lib

all: main

api.c.original: $(SDIR)/api.c
	gcc -c -fdump-tree-original-raw=api.c.original $(SDIR)/api.c $(CFLAGS)

dump.json: api.c.original 
	python3 ../cbind/parser.py api.c.original

$(SDIR)/binding.c: dump.json 
	python3 ../cbind/main.py dump.json -o $(SDIR)/binding.c

%.o: $(SDIR)/%.c $(DEPS)
	gcc -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	gcc -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean distclean

clean:
	rm -f *.o dump.json *.original src/binding.c 

distclean:
	rm -f main