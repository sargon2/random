<?
	function sum_proper_divisors($n) {
		$r = 0;
		for($i=1;$i<=($n/2);$i++) {
			if($n%$i == 0) $r += $i;
		}
		return $r;
	}
	function get_all_abundant($min, $max) {
		$ret = array();
		for($i=$min;$i<=$max;$i++) {
			if($i % 1000 == 0) print $i . "\n";
			if(sum_proper_divisors($i) > $i) $ret[$i] = true;
		}
		print count($ret) . " abundant numbers found\n";
		return $ret;
	}
	function get_all_sumoftwo($data) {
		$final = array();
		foreach($data as $x=>$ignore) {
			foreach($data as $y=>$ignore) {
				$final[$x + $y] = true;
			}
		}
		return $final;
	}
	$d = get_all_sumoftwo(get_all_abundant(12, 28123));
	$sum = 0;
	for($i=1;$i<=28123;$i++) {
		if($d[$i]) continue;
		$sum += $i;
	}
	print "sum is $sum\n";
?>
