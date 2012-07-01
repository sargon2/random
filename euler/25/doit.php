<?
	$a = "1";
	$b = "1";
	$n = 2;
	while(true) {
		$c = bcadd($a, $b);
		$n++;
		if(strlen($c) >= 1000) die($n . "\n");
		$a = $b;
		$b = $c;
	}
?>
