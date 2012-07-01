#include <pthread.h>
#include <string.h>
#include <ctype.h>
#include <cbot.h>
#include <stdlib.h>
#include <HashTable.h>

#define NICK	"chessbot"

char *hooklist[] = { "chal", NULL };
char *userlist[] = { NICK, NULL };
char *colors[] = { "4,0", /* BW - board , piece */
                   "4,1", /* BB */
                   "1,0", /* WB */
                   "0,1" }; /* WW */

typedef enum {
	P_NONE =     0,
	P_WKING =    1,
	P_WQUEEN =   2,
	P_WBISHOP =  3,
	P_WKNIGHT =  4,
	P_WROOK =    5,
	P_WPAWN =    6,
	P_BKING =    7,
	P_BQUEEN =   8,
	P_BBISHOP =  9,
	P_BKNIGHT = 10,
	P_BROOK =   11,
	P_BPAWN =   12
} piece_t;

typedef enum {
	true = 1,
	false = 0
} bool;

struct PlayerData {
	struct Game *game;
	char *nick;
	struct PlayerData *opponent;
	bool color;
	bool myturn;
};

struct Game {
	char *channel;
	piece_t board[8][8];
};

static HashTable tbl;
static pthread_mutex_t tbl_l = PTHREAD_MUTEX_INITIALIZER;

void module_init()
{
	tbl = hash_table_create();

	join(NICK, "#chess");
}

void board_init(struct Game *g)
{
	int i, j;
	for(i=0;i<8;i++) for(j=2;j<6;j++) g->board[i][j] = P_NONE;
	g->board[0][0] = g->board[7][0] = P_WROOK;
	g->board[1][0] = g->board[6][0] = P_WKNIGHT;
	g->board[2][0] = g->board[5][0] = P_WBISHOP;
	g->board[3][0] = P_WQUEEN;
	g->board[4][0] = P_WKING;
	for(i=0;i<8;i++) g->board[i][1] = P_WPAWN;

	g->board[0][7] = g->board[7][7] = P_BROOK;
	g->board[1][7] = g->board[6][7] = P_BKNIGHT;
	g->board[2][7] = g->board[5][7] = P_BBISHOP;
	g->board[3][7] = P_BKING;
	g->board[4][7] = P_BQUEEN;
	for(i=0;i<8;i++) g->board[i][1] = P_BPAWN;
}

void game_create(char *player, char *opponent, char *channel)
{
	struct PlayerData *pg, *og;
	struct Game *g;

	pg = (struct PlayerData *)palloc(sizeof(struct PlayerData));
	og = (struct PlayerData *)palloc(sizeof(struct PlayerData));
	g = (struct Game *)palloc(sizeof(struct Game));

	pg->player = strdup(player);
	og->player = strdup(opponent);
	board_init(pg->board);
	og->board = pg->board;
	pg->opponent = og;
	og->opponent = pg;
	if(rand() % 2) {
		pg->color = pg->myturn = true;
		og->color = og->myturn = false;
	} else {
		pg->color = pg->myturn = false;
		og->color = og->myturn = true;
	}

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
		privmsg(NICK, player, "Can't play with yourself");
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
		privmsg(NICK, player, format("No such nick '%s'", opponent));
		goto chal_handler_done;
	}

	game_create(player, opponent, channel);

	if(channel != NULL) 
		privmsg(NICK, channel, format("%s has challenged %s to a game of chess!", player, opponent));
	privmsg(NICK, player, format("You have challenged %s to a game of chess!", opponent));
	privmsg(NICK, opponent, format("%s has challenged you to a game of chess!", player));
/*	privmsg(NICK, player, format("Choose your weapon with /msg %s r p or s", NICK));
	privmsg(NICK, opponent, format("Choose your weapon with /msg %s r p or s", NICK));
*/

chal_handler_done:
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

void move_handler(char *source, char *msg) {
}

void draw_handler(char *source, char *dest, char *msg) {
	/* this has msg so people can !draw in-progress games */
	/* e.g. nick1 is fighting nick2, nick3 does !draw nick2 */
	bool blank = false;
	char* viewas;
	struct Game *g;
	if(msg != NULL) {
		if(!strncmp(msg, "blank", 5)) {
			blank = true;
			g = (struct Game *)palloc(sizeof(struct Game));
			board_init(g->board);
			g->color = true;
		}
		viewas = strdup(msg);
	} else {
		viewas = strdup(source);
	}

	if(blank == false) {
		pthread_mutex_lock(&tbl_l);
		if((g = hash_table_lookup(tbl, viewas)) == NULL) {
			if(msg == NULL) reply("You aren't in a game");
			else replyf("%s is not in a game", msg);
			goto draw_handler_done;
		}
	}

	if(g->color == true) reply("   A B C D E F G H");
	else reply("   H G F E D C B A");

draw_handler_done:
	if(blank == true) {
		board_destroy(g->board);
		pfree(g);
	} else {
		pthread_mutex_unlock(&tbl_l);
	}
}

bool is_legal(piece_t **board, char *move) {
	return true;
}

void privmsg_handler(char *source, char *dest, char *msg)
{
	if(!strncmp(msg, "chal ", 5))
		chal_handler(source, msg + 5, NULL);
	else if(!strcmp(msg, "quit"))
		quit_handler(source);
	else if(!strncmp(msg, "draw ", 5))
		draw_handler(source, dest, msg + 5);
	else if(!strncmp(msg, "draw", 4))
		draw_handler(source, dest, NULL);
	else
		move_handler(source, msg);
}

void hook_handler(char *hook, char *source, char *dest, char *msg)
{
	if(!strcmp(hook, "draw"))
		draw_handler(source, dest, msg);

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
