#!/usr/bin/perl -w

use Net::IRC;
use strict;

my $chan;
$chan = "#hatcave";

my $irc = new Net::IRC;

my $conn = $irc->newconn(Nick => 'echobot', Server=>'localhost', Ircname=>'echobot');

$conn->add_global_handler('376', \&on_connect);
$conn->add_global_handler('public', \&on_public);
$conn->add_handler('msg', \&on_msg);


print ("....\n");
$irc->start;

sub on_connect {
    my $self = shift;
    $self->join ($chan);
    $self->print ("joined\n");
}

sub on_msg {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    my @in = split(/ /, $arg);
    if($in[0] eq "join") {$self->join ($chan);}
}

sub on_public {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    my @in = split(/ /, $arg);

    if($in[0] eq "!echo") {
	my $rest = substr($arg, 6);
	$self->privmsg($chan, $rest);
    }
}
