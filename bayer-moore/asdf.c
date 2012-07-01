#include <stdio.h>

char peekc(FILE *fp);

int main(int argc, char **argv) {
	char needle[1024];
	int jump[256];
	int len;
	int i, j;
	FILE *fp;
	char c;

	if(argc != 3) {
		printf("Usage: %s needle file\n", argv[0]);
		exit(0);
	}
	strcpy(needle, argv[1]);

	/* Create the jump table */
	len = strlen(needle);
	for(i = 0;i<256;i++) {
		jump[i] = len;
	}

	for(i=0;i<len;i++) {
		jump[needle[i]] = (len - i) - 1;
	}

	if((fp = fopen(argv[2], "r")) == NULL) {
		perror(argv[2]);
		exit(0);
	}

	fseek(fp, len - 1, SEEK_SET);

	while(!feof(fp)) {
		c = peekc(fp);
		j = jump[c];

/*		printf("c is %c, j is %d\n", c, j);*/
		if(j == 0) {
			for(i=0;i<len-1;i++) {
				fseek(fp, -1, SEEK_CUR);
				c = peekc(fp);
/*				printf("partial match, c is %c, i is %d, n is %c\n", c, i, needle[(len - i) - 2]);*/
				if(c != needle[(len - i) - 2]) {
					fseek(fp, i, SEEK_CUR);
					i = len + 2;
					j = len;
				}

				if(i == len-2) {
					printf("Match found!\n");
					j = len;
				}
			}
		}
		if(fseek(fp, j, SEEK_CUR) != 0) {
			perror("fseek");
			exit(0);
		}
		
	}
}

char peekc(FILE *fp) {
	char c;
	c = getc(fp);
	if(feof(fp)) {
		printf("EOF\n");
		exit(0);
	}
	fseek(fp, -1, SEEK_CUR);
	return c;
}
