#!/usr/bin/perl -w
use strict;
use Net::IRC;
use sigtrap 'handler', \&signals, 'PIPE';

# Known missing events: ctcp notice invite kill wallops
# and kick is broken

# Possibly log hostmask on joins?


my $irc = new Net::IRC;
my $chan = "#testasdf";
#if(!exists($ARGV[0])) { die("Need a channel"); }
#my $chan = $ARGV[0];
#my $mynick = "alog-$chan";
my $mynick = "fire";
$mynick =~ s/[^-a-z]//g;

print "Creating connection to IRC server...\n";

#$irc->debug(1);

my $conn = $irc->newconn(Server   => 'localhost',
			 Port     => 6667,
			 Nick     => $mynick,
			 Ircname  => $mynick,
			 Username => $mynick)
    or die "irctest: Can't connect to IRC server.\n";

print "Connected";

sub signals {
	print "Socket closed! (SIGPIPE)\n";
}

sub on_init {
    my ($self, $event) = @_;
    my (@args) = ($event->args);
    shift (@args);
    $self->join($chan);
#    $self->join("#test2");
    print "*** @args\n";
}

sub on_public {
    my ($self, $event) = @_;
    my ($arg) = ($event->args);
    my ($channel) = ($event->to)[0];
    my ($nick, $mynick) = ($event->nick, $self->nick);

	if(length($arg) < 20) { return; }
	if($arg =~ /[a-z0-9]/i) { return; }
	# If the message is comprised of 4 or less characters
	# and they're not alphanumeric
	# and the line is too long..
	# Spew the same characters they're using.

     
	my $i;
	my %chars;
	my $c;
	for($i=0;$i<length($arg);$i++) {
		$c = substr($arg, $i, 1);
		$chars{$c} = $c;
	}


	my $tmp;
	my @chars2;
	foreach $tmp (values %chars) {
		$chars2[$#chars2 + 1] = $tmp;
	}
	if($#chars2 > 8) { return; }

	$chars2[$#chars2 + 1] = " ";
	$chars2[$#chars2 + 1] = " ";

	my $str = "";
	for($i=0;$i<length($arg); $i++) {
		$str .= $chars2[int rand ($#chars2+1)];
	}

	$self->privmsg($chan, $str);

}
print "Installing handler routines...";

#$conn->add_handler('cping',  \&on_ping);
#$conn->add_handler('crping', \&on_ping_reply);
#$conn->add_handler('msg',    \&on_msg);
#$conn->add_handler('chat',   \&on_chat);
$conn->add_handler('public', \&on_public);
#$conn->add_handler('caction', \&on_action);
#$conn->add_handler('join',   \&on_join);
#$conn->add_handler('part',   \&on_part);
#$conn->add_handler('cdcc',   \&on_dcc);
#$conn->add_handler('topic',   \&on_topic);
#$conn->add_handler('notopic',   \&on_topic);
#$conn->add_handler('mode',   \&on_mode);
#$conn->add_handler('nick',   \&on_nick);
#$conn->add_handler('kick',   \&on_kick);
#$conn->add_handler('quit',   \&on_quit);

$conn->add_global_handler([ 251,252,253,254,302,255 ], \&on_init);
#$conn->add_global_handler('disconnect', \&on_disconnect);
#$conn->add_global_handler(376, \&on_connect);
#$conn->add_global_handler(433, \&on_nick_taken);
#$conn->add_global_handler(353, \&on_names);

print " done.\n";

print "starting...\n";
#$irc->start;

while(1) {
	$irc->do_one_loop;
	sleep 1;
}
