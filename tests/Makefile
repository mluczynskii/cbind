ODIR=./build
IDIR=./include
SDIR=./src

LIBS=-lm -llua

_DEPS = api.h binding.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = api.o binding.o main.o
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

CC=gcc
CFLAGS=-I$(IDIR) -I/usr/local/include -L/usr/local/lib

$(ODIR)/%.o: $(SDIR)/%.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

main: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o