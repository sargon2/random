#include <pthread.h>
#include <string.h>
#include <ctype.h>
#include <cbot.h>
#include <HashTable.h>

#define NICK	"shambot"

char *hooklist[] = { "chal", NULL };
char *userlist[] = { NICK, NULL };

typedef enum {
	W_NONE = -1,
	W_ROCK = 0,
	W_PAPER = 1,
	W_SCISSORS = 2
} weapon_t;

int result_table[3][3] = {
	{ 0, -1, 1 },
	{ 1, 0, -1 },
	{ -1, 1, 0 }
};

struct Game {
	char *player;
	char *channel;
	weapon_t weapon;
	struct Game *opponent;
};

static HashTable tbl;
static pthread_mutex_t tbl_l = PTHREAD_MUTEX_INITIALIZER;

void module_init()
{
	tbl = hash_table_create();

	join(NICK, "#ro");
	join(NICK, "#realro");
	join(NICK, "#");
	join(NICK, "#gayteenchat");
}

void game_create(char *player, char *opponent, char *channel)
{
	struct Game *pg, *og;

	pg = (struct Game *)palloc(sizeof(struct Game));
	og = (struct Game *)palloc(sizeof(struct Game));

	pg->player = strdup(player);
	og->player = strdup(opponent);
	pg->weapon = W_NONE;
	og->weapon = W_NONE;
	pg->opponent = og;
	og->opponent = pg;

	if(channel != NULL) 
		pg->channel = og->channel = strdup(channel);
	else
		pg->channel = og->channel = NULL;

	hash_table_insert(tbl, player, pg);
	hash_table_insert(tbl, opponent, og);
}

void game_destroy(struct Game *g)
{
	hash_table_remove(tbl, g->player);
	hash_table_remove(tbl, g->opponent->player);

	pfree(g->opponent->player);
	pfree(g->opponent);
	pfree(g->player);

	if(g->channel != NULL) 
		pfree(g->channel);

	pfree(g);
}

static void chal_handler(char *player, char *opponent, char *channel)
{
	char *t;

	if((t = strchr(opponent, ' ')) != NULL)
		*t = '\0';

	strtolower(player);
	strtolower(opponent);

	if(!strcmp(player, opponent)) {
		privmsg(NICK, player, "Didn't your mom ever tell you it's wrong to play with yourself?");
		return;
	}

	pthread_mutex_lock(&tbl_l);

	if(hash_table_lookup(tbl, player) != NULL) {
		privmsg(NICK, player, "You are already in a game");
		goto chal_handler_done;
	}

	if(hash_table_lookup(tbl, opponent) != NULL) {
		privmsg(NICK, player, format("%s is already in a game", opponent));
		goto chal_handler_done;
	}

	if(!whois(opponent, NULL, NULL)) {
		privmsg(NICK, player, format("There's no one around here called '%s'", opponent));
		goto chal_handler_done;
	}

	game_create(player, opponent, channel);

	if(channel != NULL) 
		privmsg(NICK, channel, format("%s has challenged %s to a game of rock paper scissors!", player, opponent));
	privmsg(NICK, player, format("You have challenged %s to a game of rock paper scissors!", opponent));
	privmsg(NICK, opponent, format("%s has challenged you to a game of rock paper scissors!", player));
	privmsg(NICK, player, format("Choose your weapon with /msg %s r p or s", NICK));
	privmsg(NICK, opponent, format("Choose your weapon with /msg %s r p or s", NICK));

chal_handler_done:
	pthread_mutex_unlock(&tbl_l);
}

weapon_t get_weapon_type(char *weapon)
{
	char *t;

	if((t = strchr(weapon, ' ')) != NULL)
		*t = '\0';

	if(strlen(weapon) == 1) {
		switch(*weapon) {
			case 'r':
				return W_ROCK;
			case 'p':
				return W_PAPER;
			case 's':
				return W_SCISSORS;
			case 'R':
				return W_ROCK;
			case 'P':
				return W_PAPER;
			case 'S':
				return W_SCISSORS;
		}

		return W_NONE;
	}

	if(!strcasecmp(weapon, "rock"))
		return W_ROCK;

	if(!strcasecmp(weapon, "paper"))
		return W_PAPER;

	if(!strcasecmp(weapon, "scissors"))
		return W_SCISSORS;

	return W_NONE;
}

void weapon_handler(char *player, char *weapon)
{
	struct Game *g;
	char *winner, *loser, *t;
	weapon_t w;

	strtolower(player);

	pthread_mutex_lock(&tbl_l);
	if((g = hash_table_lookup(tbl, player)) == NULL) {
		privmsg(NICK, player, "You aren't in a game");
		goto weapon_handler_done;
	}

	if(g->weapon != W_NONE) {
		privmsg(NICK, player, "You've already selected a weapon");
		goto weapon_handler_done;
	}

	if((g->weapon = get_weapon_type(weapon)) == W_NONE) {
		privmsg(NICK, player, format("Invalid weapon: '%s'", weapon));
		goto weapon_handler_done;
	}
	
	privmsg(NICK, player, "Received your weapon choice");
	privmsg(NICK, g->opponent->player, format("Received weapon choice from %s", player));

	if(g->opponent->weapon == W_NONE)
		goto weapon_handler_done;

	switch(result_table[g->weapon][g->opponent->weapon]) {
		case -1:
			loser = player;
			winner = g->opponent->player;
			w = g->opponent->weapon;
			break;
		case 0:
			privmsg(NICK, player, "Tie, try again");
			privmsg(NICK, g->opponent->player, "Tie, try again");
			g->weapon = W_NONE;
			g->opponent->weapon = W_NONE;

			goto weapon_handler_done;
		case 1:
			loser = g->opponent->player;
			winner = player;
			w = g->weapon;
	}

	privmsg(NICK, loser, "You lose");
	privmsg(NICK, winner, "You win");

	switch(w) {
		case W_ROCK:
			t = format("%s's scissors were crushed under the weight of %s's rock", loser, winner);
			break;
		case W_PAPER:
			t = format("%s's rock was rendered non-existant by the covering power of %s's paper", loser, winner);
			break;
		case W_SCISSORS:
			t = format("%s's paper was shredded to bits by %s's scissors", loser, winner);
		case W_NONE:
	}
	
	if(g->channel != NULL) 
		privmsg(NICK, g->channel, t);
	else {
		privmsg(NICK, loser, t);
		privmsg(NICK, winner, t);
	}

	game_destroy(g);

weapon_handler_done:
	pthread_mutex_unlock(&tbl_l);
}

void quit_handler(char *player)
{
	struct Game *g;
	pthread_mutex_lock(&tbl_l);

	strtolower(player);

	if((g = hash_table_lookup(tbl, player)) == NULL) {
		privmsg(NICK, player, "You aren't in a game");
		goto quit_handler_done;
	}

	privmsg(NICK, player, "You have cancelled the game");
	privmsg(NICK, g->opponent->player, format("%s cancelled the game", player));
	if(g->channel != NULL) 
		privmsg(NICK, g->channel, format("%s cancelled the game with %s", player, g->opponent->player));

	game_destroy(g);
quit_handler_done:
	pthread_mutex_unlock(&tbl_l);
}

void privmsg_handler(char *source, char *dest, char *msg)
{
	if(!strncmp(msg, "chal ", 5))
		chal_handler(source, msg + 5, NULL);
	else if(!strcmp(msg, "quit"))
		quit_handler(source);
	else
		weapon_handler(source, msg);
}

void hook_handler(char *hook, char *source, char *dest, char *msg)
{
	if(*dest != '#' && *dest != '&')
		dest = NULL;
	
	chal_handler(source, msg, dest);
}

void nick_handler(char *old_nick, char *new_nick)
{
	struct Game *g;

	strtolower(old_nick);
	strtolower(new_nick);

	pthread_mutex_lock(&tbl_l);
	if((g = hash_table_remove(tbl, old_nick)) == NULL) 
		goto nick_handler_done;

	pfree(g->player);
	g->player = strdup(new_nick);
	hash_table_insert(tbl, new_nick, g);

nick_handler_done:
	pthread_mutex_unlock(&tbl_l);
}
