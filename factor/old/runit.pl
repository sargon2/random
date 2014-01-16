#!/usr/bin/perl -w
for($i=10001;$i<20000;$i+=2) {
	if($i % 5 == 0) {$i+=2;}
	print $i . " " . `./testr $i | tr "\n" " "`; 
	print "\n";
}
for($i=100001;$i<110000;$i+=2) {
	if($i % 5 == 0) {$i+=2;}
	print $i . " " . `./testr $i | tr "\n" " "`; 
	print "\n";
}
for($i=1000001;$i<1010000;$i+=2) {
	if($i % 5 == 0) {$i+=2;}
	print $i . " " . `./testr $i | tr "\n" " "`; 
	print "\n";
}
for($i=10000001;$i<10010000;$i+=2) {
	if($i % 5 == 0) {$i+=2;}
	print $i . " " . `./testr $i | tr "\n" " "`; 
	print "\n";
}

