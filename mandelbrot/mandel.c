#include <stdio.h>
#include <string.h>
int main(int argc, char** argv) {
	char chars[] = "..`'-,~*+:;abcdefghijklmnopqrstuvwxyz\"!|$%&()/<=>^_?@[\\]{}0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ#";
	float x0, y0;
	for(y0=-1;y0<1;y0 += 0.05) {
		for(x0=-2;x0<1;x0 += 0.05) {
			float x=0, y=0;
			int iteration = 0;
			int max_iteration = strlen(chars);

			while(x*x + y*y <= (2*2) && iteration < max_iteration) {
				float xtemp = x*x - y*y + x0;
				y = 2*x*y + y0;
				x = xtemp;
				iteration++;
			}
//			printf("iteration is %d\n", iteration);
			if(iteration == max_iteration) printf("  ");
			else printf(" %c", chars[iteration]);
//			else printf(" %c", iteration + 32);
		}
		printf("\n");
	}
}
