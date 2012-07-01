#!/usr/bin/perl -w

my $maxchars = 45;

my $counter = 0;

open FILE, "./usage";
$blah = <FILE>;
close FILE;
@ary = split(" ", $blah);

$ary[2] = 1544280 * 100;
$ary[3] = 1544280 * 100;
if($ary[0] > $ary[2]) { $ary[0] = $ary[2]; }
if($ary[1] > $ary[3]) { $ary[1] = $ary[3]; }

if($ary[2]==0) {$ary[2]=1;}
if($ary[3]==0) {$ary[3]=1;}
$str = "in:  " . bps($ary[0]) . " ]";
print $str;
$counter = 1;
for($i=0;$i<($ary[0]*$maxchars)/$ary[2];$i++) {
	print "#";
	$counter++;
}
while($counter <= $maxchars) { print "-"; $counter++; }
print "[ " . bps($ary[2]) . "\n";
$str = "out: " . bps($ary[1]) . " ]";
print $str;
$counter = 1;
for($i=0;$i<($ary[1]*$maxchars)/$ary[3];$i++) {
	print "#";
	$counter++;
}
while($counter <= $maxchars) { print "-"; $counter++; }
print "[ " . bps($ary[3]) . "\n";

sub bps {
	$blah = "bps ";
	my $num = $_[0];
	if ($num > 1024) { $num /= 1024; $blah = "kbps"; }
	if ($num > 1024) { $num /= 1024; $blah = "mbps"; }
	if ($num > 1024) { $num /= 1024; $blah = "gbps"; }
	return sprintf("%8.2f", $num) . $blah;
}
