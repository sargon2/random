<?
	$num = 10000;
	$primes = array();

	// False means prime, true means not prime

	$s = sqrt($num);
	$i = 2;
	do {
		// Find the next prime
		while(isset($primes[$i])) $i++;
		for($j=$i*2;$j<$num;$j+=$i) {
			$primes[$j] = true;
		}
		$i++;
	} while($i <= $s);

	die();

	for($i=2;$i<$num;$i++) {
		if(isset($primes[$i])) continue;
		print $i . " ";
	}
?>
