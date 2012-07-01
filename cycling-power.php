<?
	$Vg = 5; // Ground velocity
	$W = 230; // Weight, lbs (including bike)
	$K1 = .0053;
	$G = 0.07; // Grade, 0-1 (0.07 is steep)
	$K2 = .0083;
	$Va = 5; // Air velocity

	$P = ($Vg*$W*($K1+$G) + $K2*pow($Va, 3))/375;
	print "P is $P horsepower";

	print "<br>";

	$watts = $P * 745.699872;
	print "$watts watts";

	print "<br>";

	$calories = $P * 641.615568;
	print "$calories calories per hour";
?>
