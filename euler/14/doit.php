<?
	function count_terms($n) {
		$c = 1;
		do {
			if($n % 2 == 0) {
				$n /= 2;
			} else {
				$n = $n * 3 + 1;
			}
			$c++;
		} while($n != 1);
		return $c;
	}
	$max = 0;
	for($i=2;$i<1000000;$i++) {
		$c = count_terms($i);
		if($c > $max) {
			$max = $c;
			print "starting term $i has $c terms\n";
		}
	}
?>
