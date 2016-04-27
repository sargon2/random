<?
	for($i=1;$i<50;$i++) {
		print "$i: " . sum_digits($i) . "\n";
	}
	function sum_digits($n) {
		$b = pow(2, $n);
		$b = "" . $b;
		$digits = str_split($b);
		return array_sum($digits);
	}
?>
