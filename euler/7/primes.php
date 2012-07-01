<?
	$n = 1;
	for($i=2;$n<=10001;$i++) {
		if(is_prime($i)) $n++;
	}
	print $i-1 . "\n";
	function is_prime($num) {
		for($i=2;$i<=sqrt($num);$i++) {
			if($num % $i == 0) return false;
		}
		return true;
	}
?>
