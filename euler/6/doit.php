<?
	$n = 100;
	$square_of_sum = pow((($n * ($n+1))/2),2);
	$s = 0;
	for($i=1;$i<=$n;$i++) {
		$s += pow($i,2);
	}
	$d = $square_of_sum - $s;
	print "square of sum: $square_of_sum, sum of squares: $s, difference: $d\n";
?>
