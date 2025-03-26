IDIR=./include
SDIR=./src

LIBS=-lm -llua

_DEPS = api.h binding.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

OBJ = api.o binding.o main.o

CC=gcc
CFLAGS=-I$(IDIR) -I/usr/local/include -L/usr/local/lib

%.o: $(SDIR)/%.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean distclean

clean:
	rm -f *.o dump.json *.original src/binding.c 

distclean:
	rm -f main