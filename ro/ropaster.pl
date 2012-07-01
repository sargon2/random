#!/usr/bin/perl -w

use Net::IRC;
               use Text::Wrap qw(wrap $columns $huge);

               $columns = 255;
               $huge = 'wrap';


#system("rm /tmp/delme");
#system("mkfifo /tmp/delme");

$| = 1;


my $chan;
$chan = "#ro";

$irc = new Net::IRC;

$conn = $irc->newconn(Nick => 'r', Server=>'localhost', Port=> 6667, Ircname=>'r');

$conn->add_global_handler('376', \&on_connect);
$conn->add_global_handler('public', \&on_public);
$conn->add_handler('msg', \&on_msg);
$conn->add_handler('caction', \&on_caction);
$conn->add_handler('join', \&on_join);
$conn->add_handler('part', \&on_part);
$conn->add_handler('topic', \&on_topic);
$conn->add_handler('no_topic', \&on_topic);
$conn->add_handler('nick', \&on_nick);

print ("....\n");
#$irc->start;


sub on_connect {
    my $tmp;
    my $self = shift;
    $self->join ($chan);
    $self->print ("joined\n");
}

sub on_msg {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    my @in = split(/ /, $arg);
    if($in[0] eq "join") {$self->join ($chan);}
    #else {$self->nick($in[0]);}
}

sub on_public {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    write_log("<".$event->nick."> ".$arg);
	return;
	$doit = 0;
	if($arg =~ /([a-z]{3,6}:\/\/\S+)/) {
		$var = $1;
		$doit = 1;
	}
	elsif($arg =~ /([a-z]{3,6}\.(com|net|org|mil|gov|edu|biz|museum|aero|coop|info|pro|name)(\/\S+|\s|$))/i) {
		$var = "http://$1";
		$doit = 1;
	}
	elsif($arg =~ /([a-z]{3,6}\.[a-z]{2}(\/\S+|\s|$)\b)/i) {
		$var = "http://$1";
		$doit = 1;
	}
	if($doit == 1) {
		open FILE, "urls.txt";
		@arry = <FILE>;
		close FILE;
		$var =~ s/&/&amp;/g;
		$var =~ s/</&lt;/g;
		$var =~ s/>/&gt;/g;
		$var = "<a href=$var>$var</a><br>\n";
		unshift(@arry, $var);
		if($#arry >= 30) {
			$#arry = 29;
		}
		open FILE, ">urls.txt";
		print FILE @arry;
		close FILE;
		#system("./add $var");
	}
#    if($arg =~ /^!whopasted/) {
#	open FILE, "/home/sargon/whopasted";
#	$blah = <FILE>;
#	$blah =~ s/\./ /g;
#	$self->privmsg($chan, $blah);
#        write_log("<_> ".$blah);
#    }

}

sub on_caction {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    write_log(" * ".$event->nick." ".$arg);
	return;
	$doit = 0;
	if($arg =~ /([a-z]{3,6}:\/\/\S+)/) {
		$var = $1;
		$doit = 1;
	}
	elsif($arg =~ /([a-z]{3,6}\.(com|net|org|mil|gov|edu|biz|museum|aero|coop|info|pro|name)(\/\S+|\s|$))/i) {
		$var = "http://$1";
		$doit = 1;
	}
	elsif($arg =~ /([a-z]{3,6}\.[a-z]{2}(\/\S+|\s|$)\b)/i) {
		$var = "http://$1";
		$doit = 1;
	}
	if($doit == 1) {
		open FILE, "urls.txt";
		@arry = <FILE>;
		close FILE;
		$var =~ s/&/&amp;/g;
		$var =~ s/</&lt;/g;
		$var =~ s/>/&gt;/g;
		$var = "<a href=$var>$var</a><br>\n";
		unshift(@arry, $var);
		if($#arry >= 30) {
			$#arry = 29;
		}
		open FILE, ">urls.txt";
		print FILE @arry;
		close FILE;
		#system("./add $var");
	}
}

sub on_join {
    my ($self, $event) = @_;
    write_log(" *** ".$event->nick." has joined $chan");
}

sub on_part {
    my ($self, $event) = @_;
    write_log(" *** ".$event->nick." has left $chan");
}

sub on_topic {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    write_log(" *** ".$event->nick." set topic to \"$arg\"");
}

sub on_nick {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    write_log(" *** ".$event->nick." is now known as $arg");
}

sub my_ctime {
	my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	return sprintf("%02d/%02d/%02d %02d:%02d:%02d", $mon, $mday, $year - 100, $hour, $sec, $min);
}

sub write_log {
    return; # disabled since it won't log exits...hmm...
    open LOG, ">> /home/sargon/logs/ro.log";
    print LOG "[", my_ctime(), "] ", $_[0], "\n";
    close LOG;
}


$irc->do_one_loop();
$conn->join($chan);
$irc->do_one_loop();
		open FIFO, "/home/sargon/rourls";

    while(1) {
#	if ( (stat("/home/sargon/rourls"))[7]) 
{
		while ($tmp = <FIFO>) {
			chomp($tmp);
			$tmp =~ s/^\s+//;
			$tmp = wrap("","",$tmp);
			@lines = split(/\n/, $tmp);
			for($i=0;$i<=$#lines;$i++) { 
				if(($lines[$i] =~ /oatse/i) || ($lines[$i] =~ /stileproject\.com/)) {
					#$conn->privmsg($chan, "[ PASTE EDITED FOR CONTENT ]");
				}
				else
				{
				        open FILE, "/home/sargon/rowhopasted";
				        $blah = <FILE>;
					chomp($blah);
					close FILE;
					open FILE, ">/home/sargon/rowhopasted";
					print FILE " ";
					close FILE;
					open FILE, "/home/sargon/pasters";
					while($bleh = <FILE>) {
						chomp($bleh);
						@names = split(' ', $bleh);
						if($names[0] eq $blah) { $blah = $names[1]; }
					}
					close FILE;
					$blah =~ s/\./ /g;
					$blah = "<".$blah."> ";
					if(length($blah) < 5) { $blah = ""; }
					$conn->privmsg($chan, $blah.$lines[$i]);
    					write_log("<p> ".$blah.$lines[$i]);
				}
			}
        		$irc->do_one_loop();
	        }
	}
       	$irc->do_one_loop();
	sleep 1;
			
    }

	close FIFO;

