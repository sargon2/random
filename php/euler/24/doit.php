<?
	$digits = array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9);
	// 012
	// 021
	// 102
	// 120
	// 201
	// 210
	function get_next($digits) {
		$i = get_i($digits);
		$j = get_j($digits, $i);
		$t = $digits[$i];
		$digits[$i] = $digits[$j];
		$digits[$j] = $t;
		$ret = array();
		for($l = 0; $l <= $i; $l++) {
			$ret[] = $digits[$l];
		}
		for($l = sizeof($digits)-1; $l > $i; $l--) {
			$ret[] = $digits[$l];
		}
		return $ret;
	}
	function get_i($digits) {
		for($i=sizeof($digits)-2; $i > -1; $i--) {
			if($digits[$i] < $digits[$i+1]) return $i;
		}
		die("i is $i\n");
	}
	function get_j($digits, $i) {
		for($j=sizeof($digits)-1; $j > $i; $j--) {
			if($digits[$j] > $digits[$i]) return $j;
		}
		die("j is $j, i is $i\n");
	}
	$count = 1;
	while(true) {
		$digits = get_next($digits);
		$count++;
		if($count % 100000 == 0) print $count . "\n";
		if($count == 1000000) {
			print_digits($digits);
			die();
		}
	}
	function print_digits($digits) {
		foreach($digits as $digit) {
			print $digit;
		}
		print "\n";
	}
?>
