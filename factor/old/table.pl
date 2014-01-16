#!/usr/bin/perl -w

for($i = 0; $i < 10; $i++) {
	for($j = 0;$j < 10;$j++) {
		$k = $i * $j;
		if(length($k) == 1 && $ARGV[0] == 0) { $k = "0" . $k; }
		$l = substr($k, length($k)-1, 1);
		if($l == $ARGV[0]) { print "$i $j: $k\n"; }
	}
}
