<?
	ini_set('memory_limit', '256M');
	$max = 2000000;
	$nums = array_fill(2, $max - 2, true);
	$s = sqrt($max);
	foreach($nums as $k=>$v) {
		if($k > $s) break;
		for($i=$k*2;$i<$max;$i+=$k) {
			unset($nums[$i]);
		}
	}
	print array_sum(array_keys($nums)) . "\n";
?>
