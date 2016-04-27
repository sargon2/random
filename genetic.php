<?
//	$target_sequence = array(1, 2, 3, 4, 5, 6, 7);
//	$target_sequence = array(0, 1, 2, 3, 4, 5, 6, 7);
//	$target_sequence = array(0, -1, -2, -3, -4, -5, -6, -7);
//	$target_sequence = array(2, 4, 6, 8, 10, 12, 14);
//	$target_sequence = array(2, 3, 5, 7, 11, 13, 17);
	$target_sequence = array(1, 3, 7, 15, 31, 63);
//	$target_sequence = array(2, 1, 3, 2, 4, 3, 5, 4, 6, 5);
//	$target_sequence = array(50, 49, 48, 47, 46, 45);
//	$target_sequence = array(10, 9, 8, 7, 6, 5, 4);
//	$target_sequence = array(1, 1, 2, 3, 5, 8, 13, 21);
	$sequence = array();
	for($i=0;$i<50;$i++) {
		// Reproduce
		$sequences = array();
		$sequences[] = $sequence; // if no children are better...
		for($j=0;$j<1000;$j++) {
			$s = $sequence;
			$n = mt_rand(1, count($sequence) * 2 + 1);
			for($k=0;$k<=$n;$k++) {
				$s = one_mutation($s);
			}
			$sequences[] = $s;
		}
		// Calculate which one to keep
		$best_score = -1;
		$best_sequence = array();
		foreach($sequences as $curr) {
			$s = calc_score($curr, $target_sequence);
			if($s != -1) {
				if($best_score == -1 || $s <= $best_score) {
					$best_score = $s;
					$best_sequence = $curr;
					print "score progress: $best_score; ";
					print_seq($curr);
				}
			}
		}
		$sequence = $best_sequence;
		if($best_score == 1) break;
	}
	print "Target sequence: " . join(", ", $target_sequence) . "\n";
	print "Calculated sequence: ";
	for($i=0;$i<20;$i++) {
		print calculate($sequence, $i) . ",";
	}
	print "\n";
	print "Score: $best_score\n";
	print_seq($sequence);

	function print_seq($sequence) {
		foreach($sequence as $s) {
			print $s[0];
			print $s[1];
		}
		print "\n";
	}

	function calc_score($sequence, $target_sequence) {
		// If it has it exactly, use its length (shorter is better)
		// score is sum of all the diffs plus length of sequence
		$score = 0;
		foreach($target_sequence as $k=>$v) {
			$c = calculate($sequence, $k);
			if(is_nan($c)) return -1; // not valid entry
			else $score += 1000 * abs(calculate($sequence, $k) - $v);
		}
		$score += count($sequence);
		return $score;
	}

	function one_mutation($sequence) {
		if(count($sequence) == 0 || mt_rand() < mt_getrandmax() / 2) {
			// add an item
			$operators = array("*", "+", "-", "/", "^");
			// operands: numbers? 0, 1?, 'd' (current position) 'l' (calculate item at d-1)
			$operands = array("1", "2", "d", "l", "m");
			$r = array();
			$r[0] = $operators[mt_rand(0, count($operators)-1)];
			$r[1] = $operands[mt_rand(0, count($operands)-1)];
			$sequence[] = $r;
			return $sequence;
		} else {
			// remove an item
			$item = mt_rand(0, count($sequence)-1);
			array_splice($sequence, $item, 1);
			return $sequence;
		}
	}
	$memo = array();
	function calculate($sequence, $position, $reset_memo = true) {
		global $memo;
		if($reset_memo) $memo = array();
		if(isset($memo[$position])) return $memo[$position];
		if($position <= -1) return 0;
		$ret = 0;
		foreach($sequence as $s) {
			if($s[1] == 'd') $c = $position;
			else if($s[1] == 'l') $c = calculate($sequence, $position-1, false);
			else if($s[1] == 'm') $c = calculate($sequence, $position-2, false); // so it can do fibonacci
			else $c = $s[1];
			switch($s[0]) {
				case '*':
					$ret *= $c;
					break;
				case '+':
					$ret += $c;
					break;
				case '-':
					$ret -= $c;
					break;
				case '/':
					if($c != 0) 
						$ret /= $c;
					break;
				case '^':
					$ret = pow($ret, $c);
					break;
				case ' ':
				case '':
					die("weird operator\n");
					break;
			}
		}
		if(!$reset_memo) $memo[$position] = $ret;
		return $ret;
	}
?>
