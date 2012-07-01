#include <cbot.h>
#include <string.h>
#include <stdlib.h>

char *hooklist[] = { "ding", "level", NULL };

void add(char *source, char *msg)
{
	int tmp;
	tmp = atoi(msg);
	if(tmp <= 0 || tmp > 99) {
		reply("No, thank you.");
		return;
	}
	if(sql_queryf(NULL, "replace into rolevels(nick, level) values('%s','%s')", sql_escape(source), sql_escape(msg))) 
		reply("An SQL error occured");
	else
		reply("ok.");
}

void get(char *nick)
{
	void *r;
	char *t, *t2, *q;

	if(strlen(nick) > 0)
		q = format("select nick, level from rolevels where nick regexp '%s' order by level desc limit 1", sql_escape(nick));
	else
		q = format("select *, level+0 as asdf from rolevels order by asdf desc limit 1;");

	if(sql_queryf(&r, q, sql_escape(nick)) < 0) {
		replyf("No level information available for '%s'", nick);
		return;
	}

	if(sql_result_length(r) < 1) {
		reply("An SQL error occured");
		return;
	}

	if((t = sql_result_field(r, 0, 0)) == NULL) {
		reply("An SQL error occured");
		return;
	}

	if((t2 = sql_result_field(r, 0, 1)) == NULL) {
		reply("An SQL error occured");
		return;
	}
	replyf("%s: %s", t, t2);
}

void hook_handler(char *hook, char *source, char *dest, char *msg)
{
	if(!strcmp(hook, "ding"))
		add(source, msg);
	else /* level */
		get(msg);
}
