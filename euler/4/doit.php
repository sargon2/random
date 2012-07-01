<?
	$max = 0;
	$ma = 0;
	$mb = 0;
	for($i=100;$i<1000;$i++) {
		for($j=100;$j<1000;$j++) {
			$n = $i * $j;
			if(is_palindrome($n)) {
				if($n > $max) {
					$max = $n;
					$ma = $i;
					$mb = $j;
				}
			}
		}
	}
	print "$ma * $mb = $max\n";
	function is_palindrome($num) {
		if(strrev($num) == $num) return true;
		return false;
	}
?>
