<?
	error_reporting($E_ALL);
	// In order to ensure distinct states, we have two copies of the brain.
	$weights = array();
	$weights2 = array();
	$charges = array();
	$charges2 = array();

	$numnodes = 1024;

	$firethreshhold = 10;
	$splitthreshhold = 1000;
	$lowerby = 1;
	$chargeloss = 0.9;
	$inputcharge = $firethreshhold;

	function fire($from) {
		global $weights;
		global $weights2;
		global $charges;
		global $charges2;
		global $numnodes;
		global $inchar;
		global $chargeloss;

		if(($from < 512) && ($from > 256)) {
			$c = chr($from - 256);
			$inchar = $c;
			$charges2[$from] = 0;
			return;
		}


		// Figure out which node to fire to
		$max = 0;
		$matches = array();
		foreach($weights[$from] as $k=>$v) {
			if($v > $max) {
				$matches = array();
				$matches[] = $k;
				$max = $v;
			}
			if($v == $max) {
				$matches[] = $k;
			}
		}
		if($max == 0) {
			$to = mt_rand(0, $numnodes);
			if($to == $from) {
				fire($from);
				return;
			}
		} else {
			$to = $matches[mt_rand(0,count($matches))];
		}

		// Transfer charges
		$transfer = $charges[$from] * $chargeloss;
		$charges2[$to] += $transfer;
		$charges2[$from] = 0;

		// Update weights
		$weights2[$from][$to] += $transfer;
	}

	function splitit($from, $to) {
		global $weights;
		global $weights2;

		$new = makenode();
		$curr = $weights[$from][$to];
		$curr /= 2;
//		$curr = floor($curr);

		$weights2[$from][$to] = $curr;
		$weights2[$from][$new] = $curr;
	}

	function makenode() {
		global $numnodes;
		$numnodes++;
		return $numnodes;
	}

	function cycle() {
		global $weights;
		global $weights2;
		global $charges;
		global $charges2;
		global $splitthreshhold;
		global $firethreshhold;
		global $lowerby;
		global $numnodes;
		global $inchar;

		// lower weights
		foreach($weights as $k=>$v) {
			foreach($v as $k2=>$v2) {
				$weights2[$k][$k2] -= $lowerby;
				if($weights2[$k][$k2] < 0) $weights2[$k][$k2] = 0;
			}
		}

		// Create new nodes
		foreach($weights as $k=>$v) {
			foreach($v as $k2=>$v2) {
				if($v2 > $splitthreshhold) {
					splitit($k, $k2);
				}
			}
		}

		// Destroy old nodes?
		foreach($charges2 as $k=>$v) {
			if($v == 0) unset($charges2[$k]);
		}
		foreach($weights2 as $k=>$v) {
			foreach($v as $k2=>$v2) {
				if($weights2[$k][$k2] == 0) unset($weights2[$k][$k2]);
			}
		}
		foreach($weights2 as $k=>$v) {
			if(count($v) == 0) unset($weights2[$k]);
		}

		// Fire nodes (Has to be after create since it calls readchar())
		foreach($charges as $k=>$v) {
			if($v >= $firethreshhold) {
				fire($k);
			}
		}

		$weights = $weights2;
		$charges = $charges2;

//		print "End of cycle, numnodes is $numnodes\n";

		if(isset($inchar)) {
//			print "Output: '$inchar'\n";
			print $inchar;
			readchar($inchar);
			unset($inchar);
		}

	}

	function init() {
	}

	function readchar($c) {
		global $charges2;
		global $inputcharge;
//		print "Input: $c\n";
		$charges2[ord($c)] += $inputcharge;
		cycle();

		for($i=0;$i<10;$i++) {
			if(mt_rand(0,1)<0.5) cycle();
		}
	}

	function readstr($str) {
		for($i=0;$i<strlen($str);$i++) {
			$c = substr($str, $i, 1);
			print $c;
			readchar($c);
		}
	}

	init();
	readstr("I am the very model of a modern major general.\nI've information animal, vegetable and mineral.\n");
?>
