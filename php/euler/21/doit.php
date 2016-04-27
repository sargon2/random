<?
	$d = array();
	for($i=1;$i<10000;$i++) {
		$s = sum_proper_divisors($i);
		$s2 = sum_proper_divisors($s);
		if($s == $s2) continue;
		if($s2 == $i) {
			print "$i and $s\n";
			$d[$i] = true;
			$d[$s] = true;
		}
	}
	$tot = 0;
	foreach($d as $k=>$v) {
		if($v == true) $tot += $k;
	}
	print "tot is $tot\n";
	function sum_proper_divisors($n) {
		$r = 0;
		for($i=1;$i<=($n/2);$i++) {
			if($n%$i == 0) $r += $i;
		}
		return $r;
	}
?>
