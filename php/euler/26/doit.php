<?
	$max_cycle = 0;
	$max_cycle_i = 0;
	for($q=2;$q<1000;$q++) {
		$p = 1;
		//$q = 7;
		$r = $p;
		$states = array();
		$s = 0;
		while(true) {
			if(isset($states[$r])) {
				$s2 = $states[$r];
				$s2 = $s - $s2;
				print "$q - cycle of length $s2\n";
				if($s2 > $max_cycle) {
					$max_cycle = $s2;
					$max_cycle_i = $q;
				}
				break;
			}
			$states[$r] = $s;
			$s++;
			$d = (int) (($r*10) / $q);
			$r = (($r*10) % $q);
			//print $d;
		}
	}
	print "cycle of length $max_cycle at 1/$max_cycle_i\n";
?>
