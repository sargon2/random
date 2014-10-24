<?
	$ops = array(0);

	$sequence = array(1, 3, 6, 9);

	$curr=0;
	for($i=0;$i<1000000;$i++) {
		$a = count($ops);
		if($curr != $a) {
			$curr = $a;
			print "Num of ops: $curr\n";
		}
		if(test_ops($ops, $sequence) == true) {
			print "Found one: "; print_ops($ops);
		}
		$ops = increment_ops($ops);
	}

	print "Finished\n";

	function print_ops($ops) {
		print "ops: ";
		foreach($ops as $v) {
			print "$v ";
		}
		print "\n";
	}

	function increment_ops($ops) {
		$max_op = 2;
		$roll = true;
		$pos = 0;
		while($roll == true) {
			if($ops[$pos] == $max_op) {
				$ops[$pos] = 0;
				$pos++;
			} else {
				$ops[$pos]++;
				$roll = false;
			}
		}
		return $ops;
	}

	function test_ops($ops, $sequence) {
		$i = 0;
		foreach($sequence as $v) {
			$num = $i;
			foreach($ops as $op) {
				$num = performop($num, $op, $i);
			}
			if($v != $num) return false;
			$i++;
		}

		return true;
	}

	function performop($num, $op, $d) {
		switch($op) {
			case 0: $num++; break;
			case 1: $num += $d; break;
			case 2: $num <<= 1; break;
			case 3: $num--; break;
			case 4: $num >>= 1; break;
			case 5: $num -= $d; break;
			default: die("Invalid op $op\n");
		}
		return $num;
	}
?>
