#!/usr/bin/gccstream -Wall -O3
#include <stdio.h>

int main(int argc, char **argv) {
	int i;
	for(i=0;i<argc;i++) {
		printf("Argument %d: %s\n", i, argv[i]);
	}
	return 1;
}

