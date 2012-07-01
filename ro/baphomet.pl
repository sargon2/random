#!/usr/bin/perl -w

use Net::IRC;
# use Lingua::Ispell qw( spellcheck );
# Lingua::Ispell::allow_compounds(1);
# $Lingua::Ispell::path='/usr/bin/ispell';
# use Lingua::Ispell qw( add_word_lc );
# use Lingua::Ispell qw( save_dictionary );
my %sayings;
my %seen;
my %seen2;
my %next;
my %ding;
my %timer;
my %timernicks;
my %points;
my %pointsnicks;
my $lasttime;
my $thump1=0;
my $thump2=0;
my $points=0;

my $key;
my $say;

my $chan;
$chan = "#ro";

$irc = new Net::IRC;

$conn = $irc->newconn(Nick => 'baphomet', Server=>'bigfeh', 
Ircname=>'baphomet');

$conn->add_global_handler('376', \&on_connect);
$conn->add_global_handler('public', \&on_public);
$conn->add_handler('msg', \&on_msg);
$conn->add_handler('caction', \&on_caction);

print ("....\n");
#$irc->start;

sub on_connect {
    my $self = shift;
    $self->join ($chan);
    $self->print ("joined\n");
}

sub on_msg {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    my @in = split(/ /, $arg);
    my $nick = $event->nick;

# next --------------

    if((lc($in[0]) eq "next") || (lc($in[0]) eq "!next")) {
	shift(@in);
	my $whoto = shift(@in);
	my $stuff = join(" ", @in);
	$next{$whoto} .= "[" . scalar(localtime) . "] " . $whoto . ": <" . $event->nick . "> " . $stuff . "\n";
	$self->privmsg($event->nick, "k, messaging '$stuff' next time $whoto speaks");
	return;
    }

    foreach $key (keys %next) { eval {
	if($event->nick =~ /$key/i) {
	    my @temp = split("\n", $next{$key});
	    foreach $asdf (@temp) {$self->privmsg($event->nick, $asdf);}
	    delete $next{$key};
	}
    }
    }

    if(lc($in[0] eq "check")) { return; }

# quotebot --------------------
    if($in[0] eq "quote") {
        my $blah;
        if((time() - $lasttime) < 30) {
            #$self->privmsg($event->nick, 30 - (time() - $lasttime) . " seconds left before public quote");
            $blah = $event->nick;
        } else {
            $blah = $event->nick;
            $lasttime = time();
        }
        my @ary;
        if ($in[1]) {
            shift @in;
            my $tmp = join(" ", @in);
            $tmp =~ s/\`//g;
            $tmp =~ s/\'//g;
            $tmp =~ s/\"//g;
            $tmp =~ s/\;//g;
            open FL, "egrep -r -h -i '$tmp' /home/talon/eggdrop/mel/logs/*linux*|grep -v '\!quote'|grep -v '<thumper>'|"; 
            #$self->privmsg($blah, "egrep -r -h -i '$tmp' /home/talon/eggdrop/mel/logs/*linux*|grep -v '\!quote'|grep -v '<thumper>'|"); 
            if(@ary = <FL>) { 
		$send = $ary[int rand $#ary];
		if(length($send) >= 80) {$blah = $event->nick;}
		$self->privmsg($blah, $send);
	    } else {
		$self->privmsg($blah, "no match");
	    }
        }
        else {
            open FL, "grep -r -h '' /home/talon/eggdrop/mel/logs/*linux*|grep -v '\!quote'|grep -v '\<thumper\>'|"; @ary = <FL>;
		$send = $ary[int rand $#ary];
		if(length($send) >= 80) {$blah = $event->nick;}
	    $self->privmsg($blah, $send);
        }
close FL;
	return;
    }
# end quotebot -----------------

# timer --------------
    if(lc($in[0]) eq "say") {
        shift(@in);
        my $blah = shift(@in);
	if($blah =~ /\:.*\:/) {
	    ($hr, $min, $sec) = split(/\:/, $blah);
	    $blah = ($hr * 3600) + ($min * 60) + $sec;
	}
	elsif($blah =~ /\:/) {
	    ($min, $sec) = split(/\:/, $blah);
	    $blah = ($min * 60) + $sec;
	}
	$self->privmsg($event->nick, "saying '".join(" ", @in)."' in $blah seconds");
        $timer{$blah + time()} = "<".$event->nick."> ".join(" ", @in);
	$timernicks{$blah + time()} = $event->nick;
	return;
    }

# fortune ---------
    my $tmp;
    if(lc($in[0]) eq "fortune") {
        open FL, "/usr/games/fortune -s|";
        while($tmp = <FL>) {$self->privmsg($event->nick, $tmp);}
	close FL;
	return;
    }

# seen -----------------------
    if(lc($in[0]) eq "seenb") {
        $pattern = $in[1];
	readSeen();
        @match = grep { /$pattern/i } keys %seen;
        if(@match) {
        #if($seen{lc($in[1])}) {
            @eldest = sort { $seen2{$b} <=> $seen2{$a} } @match;
            my $elap = time() - $seen2{$eldest[0]};
            $blah = "[";
            $blah .= int($elap/3600) . "h ";
            $elap -= int($elap/3600) * 3600;
            $blah .= int($elap/60) . "m ";
            $elap -= int($elap/60) * 60;
            $blah .= $elap . "s ago] " . $seen{$eldest[0]};
        }
        else {
            $blah = "$in[1] has not spoken since I was started";
        }
        $self->privmsg($event->nick, $blah);
	return;
    }

# thumper -------------------
    if(lc($in[0]) eq "thump1asdf") {
	if($thump1==0) {
	    $thump1 = 1;
	    $self->privmsg($chan, "random thumping is now on (request by ".$event->nick.")");
        } else {
	    $self->privmsg($chan, "no more random thumping (request by ".$event->nick.")");
	    $thump1 = 0;
	}
	return;
    }
    if(lc($in[0]) eq "thump2asdf") {
	if($thump2==0) {$thump2 = 1;$self->privmsg($chan, "requested thumping is now on (request by ".$event->nick.")");} else {
	$self->privmsg($chan, "no more requested thumping (request by ".$event->nick.")");$thump2 = 0;}
	return;
    }


# -------------
    if($in[0] eq "join") {$self->join ($chan); return;}
    elsif($in[0] eq "add") {add_word_lc($in[1]);save_dictionary();$self->privmsg($nick, "$in[1] added");return;}
# repeatbot ------------------
    elsif(lc($in[0]) eq "repeat") {
        shift @in;
        $key = $in[0];
        shift @in;
        $say = join(" ", @in);
        $sayings{$key} = $say;
        $self->privmsg($event->nick, "repeating '$say' when someone says '$key'");
        $self->privmsg($chan, "repeating '$say' when someone says '$key' at ".$event->nick."'s request");
        return;
    }
    elsif(lc($in[0]) eq "clear") {
        undef %sayings;
        $self->privmsg($event->nick, "cleared");
        return;
    }
    elsif(lc($in[0]) eq "status") {
        foreach $key (keys %sayings) {
            $self->privmsg($event->nick, "$key: $sayings{$key}");
        }
    }
    elsif(lc($in[0]) eq "help") {
	my $help;
	open HELP, "./thumper.help";
	while($help = <HELP>) {
	    $self->privmsg($event->nick, $help);
	}
	close HELP;
        return;
    }
# end repeatbot -------------------

if($in[0] eq "pointson") {
	$points = 1;
	$self->privmsg($chan, $event->nick . " turned on the point system");
	return;
}
if($in[0] eq "pointsoff") {
	$points = 0;
	$self->privmsg($chan, $event->nick . " turned off the point system");
	return;
}
# spellbot ------------------
	return;
    my $bad = 0;
    for my $r ( spellcheck( $arg ) ) {
        if ( $r->{'type'} eq 'ok' ) {
            $self->privmsg($nick, "'$r->('term'} was found in the dictionary.\n");
        }
        elsif ( $r->{'type'} eq 'root' ) {
            $self->privmsg($nick, "'$r->{'term'}' can be formed from root '$r->{'root'}'\n");
        }
        elsif ( $r->{'type'} eq 'miss' ) {
            $self->privmsg($nick, "'$r->{'term'}' was not found in the dictionary.\n");
            $self->privmsg($nick, "Near misses: @{$r->{'misses'}}\n");
	    $bad = 1;
        }
        elsif ( $r->{'type'} eq 'guess' ) {
            $self->privmsg($nick, "'$r->{'term'} was not found in the dictionary.\n");
            $self->privmsg($nick, "Root/affix Guesses: @($r->{'guesses'})\n");
	    $bad = 1;
        }
        elsif ( $r->{'type'} eq 'compound' ) {
            $self->privmsg($nick, "'$r->{'term'} is a valid compound word\n");
        }
        elsif ( $r->{'type'} eq 'none' ) {
            $self->privmsg($nick, "No match for term '$r->{'term'}'\n");
	    $bad = 1;
        }
    }
    if($bad==0) {$self->privmsg($nick, "You got it right.");}

}

sub on_public {
    my ($self, $event) = @_;
    my ($arg) = $event->args;
    my @temp = split(/ /, $arg);
    my $tmp = $temp[int rand $#temp];
    my @in = split(/ /, $arg);

# seen shit has to be first
    $seen{lc($event->nick)} = "<".$event->nick."> $arg";
    $seen2{lc($event->nick)} = time();
    writeSeen();

# next --------------------

    foreach $key (keys %next) { eval {
	if($event->nick =~ /$key/i) {
	    my @temp = split("\n", $next{$key});
	    foreach $asdf (@temp) {$self->privmsg($event->nick, $asdf);}
	    delete $next{$key};
	}
    }
    }
    if(lc($in[0]) eq "!nextb") {
	shift(@in);
	my $whoto = shift(@in);
	my $stuff = join(" ", @in);
	$next{$whoto} .= "[" . scalar(localtime) . "] " . $whoto . ": <" . $event->nick . "> " . $stuff . "\n";
	$self->privmsg($event->nick, "k, messaging '$stuff' next time $whoto speaks");
    }

# denied ----------
    if(lc($in[0]) eq "!quote") {
	$self->privmsg($event->nick, "!quote has been disabled, please msg me quote <regex>.");
    }

    if(lc($in[0]) eq "!say") {
	$self->privmsg($event->nick, "!say has been disabled, please msg me instead.");
    }

# stats -----------------
    if((lc($in[0]) eq "!stats") || (lc($in[0]) eq "!stat")) {
	shift(@in);
	my $stuff = join(" ", @in);
	if($stuff) {
		open STATS, "stats.txt";
		my @stats = <STATS>;
		my $hit = 0;
		for($i=0;$i<$#stats;$i++) {
			eval { if($stats[$i] =~ /^[^a-z]{0,3}$stuff/i) {
			    $self->privmsg($chan, $stats[$i]);
			    $i = $#stats+1; $hit = 1;
			} }
		}
		if($hit == 0) {$self->privmsg($chan, "No match for " . $stuff);}
		close STATS;
	} else {
		$self->privmsg($chan, "!stats: show you stats on an RO monster");
	}
    }

# drops -----------------
    if((lc($in[0]) eq "!drops") || (lc($in[0]) eq "!drop")) {
	shift(@in);
	my $stuff = join(" ", @in);
	if($stuff) {
		open DROPS, "drops.txt";
		my @stats = <DROPS>;
		my $hit = 0;
		for($i=0;$i<$#stats;$i++) {
			eval { if($stats[$i] =~ /^[^a-z]{0,3}$stuff/i) {
			    $self->privmsg($chan, $stats[$i]);
			    $i = $#stats+1; $hit = 1;
			} }
		}
		if($hit == 0) {$self->privmsg($chan, "No match for " . $stuff);}
		close DROPS;
	} else {
		$self->privmsg($chan, "!drops: show you what items an RO monster drops");
	}
    }

# whodrops -----------------
    if((lc($in[0]) eq "!whodrops") || (lc($in[0]) eq "!whodrop")) {
        shift(@in);
        my $stuff = join(" ", @in);
        if($stuff) {
                open DROPS, "whodrops.txt";
                my @stats = <DROPS>;
                my $hit = 0;
                for($i=0;$i<$#stats;$i++) {
                        eval { if($stats[$i] =~ /^[^a-z]{0,3}$stuff/i) {
                            $self->privmsg($chan, $stats[$i]);
                            $i = $#stats+1; $hit = 1;
                        } }
                }
                if($hit == 0) {$self->privmsg($chan, "No match for " . $stuff);}
                close DROPS;
        } else {
                $self->privmsg($chan, "!whodrops: find out what RO monster drops an item");
        }
    }

# ding --------------------
    if(lc($in[0]) eq "!ding") {
	shift(@in);
	$stuff = join(" ", @in);

	my $blah;
	my $bleh;

	if(
	($event->nick =~ /cy/i) || 
	($event->nick =~ /yab/i) || 
	($stuff =~ /(a|4)nu(z|s)/i) || 
	($stuff =~ /f(4|a)rt/i) || 
	($stuff =~ /p(o|0){2,}p/i) ||
	(int(substr($stuff, 0, 2)) > 70) ||
	(int(substr($stuff, 0, 2)) == 0)) {
		$self->privmsg($chan, "Access denied");
	} else {

	open LEVEL, "levels.txt";
	while($blah = <LEVEL>) {
		chomp($blah);
		$blah = lc($blah);
		$bleh = <LEVEL>;
		chomp($bleh);
		$ding{$blah} = $bleh;
	}
	close LEVEL;
	$ding{lc(substr($event->nick, 0, 3))} = $stuff . " (" . $event->nick . ")";

        open LEVEL, ">levels.txt";
        foreach $key (keys %ding) {
            print LEVEL "$key\n" . $ding{$key} . "\n";
        }
        close LEVEL;
 
	$self->privmsg($chan, "ok");
    }
}

# level -------------------
    if(lc($in[0]) eq "!level") {
	my $hit = 0;
	shift(@in);
	$stuff = join(" ", @in);

	$stuff =~ s/\*//g;


	my $blah;
	my $bleh;
	my $stuff2;

        open LEVEL, "levels.txt";
        while($blah = <LEVEL>) {
                chomp($blah);
		$blah = lc($blah);
                $bleh = <LEVEL>;
		chomp($bleh);
                $ding{$blah} = $bleh;
        }
        close LEVEL;
	
	my $max = 0;


	if(!$stuff) {
		my $nk = substr($event->nick, 0, 3);
		my $nklv;
		my $place=1;
  	        foreach $key (keys %ding) {
		    if(($key =~ /^$nk/i) && ($hit == 0)) {
			$nklv = int(substr($ding{$key}, 0, 2));
			$hit = 1;
		    }
		}
		foreach $key (keys %ding) {
			if(int(substr($ding{$key}, 0, 2)) > int(substr($max, 0, 2))) {
				$max = $ding{$key};
			}
			if(int(substr($ding{$key}, 0, 2)) > $nklv) { $place++; }
		}
		$self->privmsg($chan, "$max appears to be the highest, you are in $place place");
	} else {

	$stuff2 = substr($stuff, 0, 3);

        foreach $key (keys %ding) {
	    if(($key =~ /$stuff2/i) && ($hit == 0)) {
		$self->privmsg($chan, $ding{$key});
		$hit = 1;
	    }
	}
	if($hit == 0) { $self->privmsg($chan, "No match for $stuff"); }
	}
    }

# seen -----------------------
    if(lc($in[0]) eq "!seenb") {
        $pattern = $in[1];
	readSeen();
        eval { @match = grep { /$pattern/i } keys %seen; };
        if(@match) {
        #if($seen{lc($in[1])}) {
	    @eldest = sort { $seen2{$b} <=> $seen2{$a} } @match;
            my $elap = time() - $seen2{$eldest[0]};
            $blah = "[";
            $blah .= int($elap/3600) . "h ";
            $elap -= int($elap/3600) * 3600;
            $blah .= int($elap/60) . "m ";
            $elap -= int($elap/60) * 60;
            $blah .= $elap . "s ago] " . $seen{$eldest[0]};
        }
        else {
            $blah = "$in[1] has not spoken since I was started";
        }
        $self->privmsg($chan, $blah);
    }

# thumper ----------------------------

    #if($arg =~ /\*([^\*]+)\*/ && $arg !~ /[;~\$%@\(\)&#\{\}\[\]]/) {
    if(($arg =~ s/\*([^\*]+)\* \*//g)&&($thump2==1)) {
        if(length($1) < 12) {
            $self->privmsg($chan, "*$1* *$1* *$1*");
        }
    }
    elsif(( int(rand 90) == 0 && length($tmp) > 3 && length($tmp) < 12 )&&($thump1==1)) {
        $tmp =~ s/^\*|\*$//g;
        $tmp =~ s/[^a-zA-Z0-9\s]//g;
        $self->privmsg($chan, "*$tmp* *$tmp* *$tmp*");
    }
# end thumper ---------------------------
# repeatbot --------------------------

    foreach $key (keys %sayings) {
        if($arg =~ $key) {
            $self->privmsg($chan, $sayings{$key});
        }
    }

# end repeatbot ----------------------

if($points == 1) {

    if($in[0] eq "!++") {
	if($pointsnicks{lc($in[1])} ne $event->nick) { $points{lc($in[1])}++; }
	$self->privmsg($chan, $in[1] . " has " . $points{lc($in[1])} . " points");
	$pointsnicks{lc($in[1])} = $event->nick;
    }
    if($in[0] eq "!--") {
	if($pointsnicks{lc($in[1])} ne $event->nick) { $points{lc($in[1])}--; }
	$self->privmsg($chan, $in[1] . " has " . $points{lc($in[1])} . " points");
	$pointsnicks{lc($in[1])} = $event->nick;
    }
}
    if($in[0] eq "!==") {
	$points{lc($in[1])} += 0;
	$self->privmsg($chan, $in[1] . " has " . $points{lc($in[1])} . " points");
    }

}

sub on_caction {
    my ($self, $event) = @_;
    my ($arg) = $event->args;

    $seen{lc($event->nick)} = "* ".$event->nick." $arg";
    $seen2{lc($event->nick)} = time();
    writeSeen();
}

sub writeSeen {
    open SEEN, ">/home/sargon/ro/seen.dat";
    foreach $key (keys %seen) {
	print SEEN "$key", "\n", $seen{$key}, "\n", $seen2{$key}, "\n";
    }
    close SEEN;
}

sub readSeen {
    open SEEN, "/home/sargon/ro/seen.dat";
    while ($line = <SEEN>) {
	chomp($line); $stuff[0] = $line;
	$line = <SEEN>; chomp($line); $stuff[1] = $line;
	$line = <SEEN>; chomp($line); $stuff[2] = $line;
	$seen{$stuff[0]} = $stuff[1];
	$seen2{$stuff[0]} = $stuff[2];
    }
    close SEEN;
}

readSeen();

$irc->do_one_loop();
$conn->join($chan);

# main loop
while(1)
{
    # check timers...
    foreach $key (keys %timer) {
        if($key <= time()) {
            $conn->privmsg($timernicks{$key}, $timer{$key});
            delete $timer{$key};
        }
    }
    $irc->do_one_loop();
    sleep 1;
}
