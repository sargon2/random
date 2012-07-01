#include <stdio.h>
#include <signal.h>
#include <readline/readline.h>
#include <readline/history.h>

void signals(int);

int main(int argc, char* argv[])
{
	int i;
	char prompt[] = "$ ";
	char* line;
	for(i=0;i<25;i++) {
		signal(i, signals);
	}
	rl_bind_key ('\t', rl_insert);

	for(;;) {
		line = readline(prompt);
		if(line == NULL) exit(0);
		if(strlen(line) == 4) {
			if(strncmp(line, "exit", 4) == 0) exit(0);
			if(strncmp(line, "quit", 4) == 0) exit(0);
		}
		if(strlen(line) >= 1 ) printf("fuck you\n");
	}
}

void signals(int asdf){
}
