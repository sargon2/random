<?
	$max = 100;
	$terms = array();
	for($a = 2; $a <= $max; $a++) {
		for($b = 2; $b <= $max; $b++) {
			$terms[] = bcpow($a, $b);
		}
	}
	sort($terms);
	$terms = array_unique($terms);
	print count($terms);
?>
