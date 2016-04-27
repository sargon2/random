<?
	function gcd($a, $b) {
		while($b != 0) {
			$t = $b;
			$b = $a % $b;
			$a = $t;
		}
		return $a;
	}
	function lcm($a, $b) {
		return ($a * $b) / gcd($a, $b);
	}
	$r = 1;
	for($i=2;$i<20;$i++) {
		$r = lcm($r, $i);
	}
	print $r . "\n";
?>
