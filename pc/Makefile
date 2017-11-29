CC=gcc
CFLAGS=-ansi -pedantic -Wall -Wextra -Werror
LDFLAGS=
EXEC=main
SOURCES=$(wildcard *.c)
OBJECTS=$(SOURCES:.c=.o)

$(EXEC): $(OBJECTS)
	$(CC) $(OBJECTS) -o $(EXEC) $(LDFLAGS)

%.0: %.c
	$(CC) -c $(CFLAGS) $< -o $@

clean:
	rm -f $(EXEC) $(OBJECTS)
