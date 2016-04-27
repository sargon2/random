<?
	$num = 1;
	$sum = $num;
	$size = 1001;
	$max = ($size - 1);
	for($step = 2; $step <= $max; $step += 2) {
		for($i=0;$i<4;$i++) {
			$num += $step;
			$sum += $num;
		}
	}
	print "sum is $sum\n";
?>
