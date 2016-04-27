<?
	$target = 5;
	// Figure out largest number we need to go to
	$largest_onedigit = pow(9, $target);
	$num_digits = 0;
	do {
		$num_digits++;
		$min = pow(10, $num_digits);
		$max = $largest_onedigit * $num_digits;
	} while($min < $max);
	print "max is $max\n";
	$sum = 0;
	for($i=10;$i<=$max;$i++) {
		if(is_weird($i)) {
			print $i . "\n";
			$sum += $i;
		}
	}
	print "sum is $sum\n";
	function is_weird($i) {
		global $target;
		$digits = str_split($i);
		$c = 0;
		foreach($digits as $d) {
			$c += pow($d, $target);
		}
		if($c == $i) return true;
		return false;
	}
?>
