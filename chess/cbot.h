#include <stdio.h>

/* IRC functions */
void (*replyp)(const char *message);
void (*replypf)(const char *format, ...);
void (*reply)(const char *message);
void (*replyf)(const char *format, ...);
void (*privmsg)(const char *nick, const char *dest, const char *message);
void (*notice)(const char *nick, const char *dest, const char *message);
void (*topic)(const char *channel, const char *topic);
void (*mode)(const char *channel, const char *mode);
int (*whois)(const char *nick, char **ident, char **name);
void (*join)(const char *nick, const char *channel);
void (*part)(const char *nick, const char *channel);
char *(*primary_nick)();

/* String mangling functions */
char *(*format)(const char *str, ...);
char *(*dupstr)(const char *str);
char *(*urlencode)(const char *str); 
char *(*sql_escape)(const char *string);
char *(*strtolower)(char *string);

/* Memory management functions */
void *(*aalloc)(int size);
void *(*palloc)(int size);
void *(*pfree)(void *ptr);
void *(*mkpersist)(void *ptr);

/* Process management functions */
int (*program_exec)(const char *path, char *const argv[], FILE **in, FILE **out);
void (*program_close)(int pid);

/* Socket functions */
void *(*sconnect)(char *hostname, int port);
char *(*sread)(char *socket);
int (*swrite)(void *socket, char *str);

/* SQL functions */
int (*sql_query)(void **r, const char *query);
int (*sql_queryf)(void **r, char *format, ...);
int (*sql_result_length)(void *r);
char *(*sql_result_field)(void *r, int rownum, int colnum);

/* Module management function */
int (*load_module)(char *name, char **error);
int (*unload_module)(char *name);
char *(*get_global_hooklist)();
void (*get_short_help)(char *hook);
void (*get_long_help)(char *hook);

/* I/O multiplexing functions */
#define MPLX_RD         1
#define MPLX_WR         2
#define MPLX_EX         4

void (*add_mplx_fd)(int fd, int events);
void (*remove_mplx_fd)(int fd, int events);
