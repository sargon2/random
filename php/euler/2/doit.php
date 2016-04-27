<?
	$a = 1;
	$b = 1;
	$sum = 0;
	while($a < 4000000) {
		$c = $a;
		$a += $b;
		$b = $c;
		if($a % 2 == 0) $sum += $a;
	}
	print $sum . "\n";
?>
