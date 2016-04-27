<?
	for($a=0;$a<500;$a++) {
		for($b=0;$b<500;$b++) {
			$c = sqrt(pow($a, 2) + pow($b ,2));
			if($c != floor($c)) continue;
			if($a + $b + $c == 1000) {
				$sum = $a + $b + $c;
				$prod = $a * $b * $c;
				print "a $a, b $b, c $c, sum $sum, prod $prod\n";
			}
		}
	}
?>
