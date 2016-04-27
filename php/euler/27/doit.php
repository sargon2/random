<?
	$max = -1;
	for($a=-999;$a<1000;$a++) {
		print "a is $a\n";
		for($b=-999;$b<1000;$b++) {
			$n = get_num_primes($a, $b);
			if($n > $max) {
				print "new max; a is $a, b is $b, max is $n\n";
				$max = $n;
				$max_a = $a;
				$max_b = $b;
			}
		}
	}
	$prod = $max_a * $max_b;
	print "final max $max, a is $max_a, b is $max_b, prod is $prod\n";
	function get_num_primes($a, $b) {
		$n = 0;
		while(true) {
			$value = calc_value($n, $a, $b);
			if(!is_prime($value)) return $n;
			$n++;
		}
	}
	function calc_value($n, $a, $b) {
		return pow($n, 2) + $a * $n + $b;
	}
	function is_prime($num) {
		if($num <= 0) return false;
		for($i=2;$i<=sqrt($num);$i++) {
			if($num % $i == 0) return false;
		}
		return true;
	}
?>
