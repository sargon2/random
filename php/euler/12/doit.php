<?
	function count_factors($n) {
		$s = sqrt($n);
		$c = 2; // 1 and $n
		for($i=2;$i<$s;$i++) {
			if($n % $i == 0) $c+=2;
		}
		if($s == floor($s)) $c++;
		return $c;
	}
	$i = 0;
	$c = 0;
	$max_count = 0;
	while(true) {
		$i++;
		$c += $i;
		$count = count_factors($c);
		if($count > 500) exit($c . "\n");
		if($count > $max_count) {
			print "progress: $c has $count factors\n";
			$max_count = $count;
		}
	}
?>
