CC=gcc
CFLAGS=-g -Wall -Werror -pedantic -std=gnu99 -I./lib
LDFLAGS=-L. -Wl,-rpath,.
TARGET=etovucca # Your executable name
SRCDIR=src                   # Source directory
LIBDIR=lib                   # Library directory
DEPS=Database.o libsqlite3.so # Dependencies

.PHONY: all clean initdb cgi

# Main targets:
all: $(TARGET)

cgi: etovucca # Runs Python HTTP server for CGI
		python3 -m http.server --cgi

# Building the main executable
etovucca: $(DEPS) $(SRCDIR)/RTBB.c
		$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ -lsqlite3

# Building the database object file
Database.o: $(SRCDIR)/Database.c
		$(CC) $(CFLAGS) -o $@ -c $^
		
# Building SQLite library
libsqlite3.so: $(LIBDIR)/sqlite3.c
		$(CC) -shared -o $@ -fPIC $^ -ldl -pthread
		$(CC) -o sqlite3 $^ $(LIBDIR)/shell.c -ldl -pthread

clean:
		$(RM) $(TARGET) $(DEPS) sqlite3 *.o

initdb:
		echo .quit | ./sqlite3 -init setup.sql rtbb.sqlite3
