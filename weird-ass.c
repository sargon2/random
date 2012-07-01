#include <stdio.h>

// The problem presented here is predicting what affects the memory address of str.
// We're only overwriting a single byte of memory, and with a null, so why does str change so erratically?
// Also, why doesn't it segfault until program termination?

int fn();

int main(void) {
	char str[64];
	bzero(str, 64);

	printf("str is %s, located at %x\n", str, &str);
	fn();
	printf("str is %s, located at %x\n", str, &str);
}

int fn() {
	char r;
	char *p = &r;
	*p = 'a';
	p++;
	*p = '\0'; // Deliberately write to unallocated memory
}
	

