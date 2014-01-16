<?
	function find_next_point_coord($p1, $p2, $n1, $n2) {
		// p1 is x- or y- coord, p2 is second matching
		// n1 is the period that the first plane repeats in
		// n2 is the ^^ ... second

		// the maximum t value is (n2*n1)/n2 = n1
		$t = 0;

//		print "find_next_point_coord($p1, $p2, $n1, $n2) "; flush();

		do {
			$ret = $p1 + (($p2 - $p1) % $n2) + ($t * $n2);
			$t++;
			if($ret > $n1 * $n2) {
				die("warning: ret too big: $ret in $n1 * $n2 ($p1 $p2 $n1 $n2)\n");
			}
		} while ($ret % $n1 != $p1 || $ret % $n2 != $p2);

//		print "returning $ret\n"; flush();

		global $num_to_factor;

		test_match($ret, $num_to_factor);

		return $ret;
		// increment t until...
		// ret % n1 = p1
		// ret % n2 = p2
	}

//	$num_to_factor = 121;
//	$num_to_factor = 1313;
//	$num_to_factor = 297937;
//	$num_to_factor = 2062087;
	$num_to_factor = 62615533;
//	$num_to_factor = 212051843;
//	$num_to_factor = 3015986723;

	$curr = new bitplane();

	$small_primes = array(2, 3, 5, 7, 11, 13, 17, 19); // todo: calculate this instead of hardcoding it
	$loc = 0;

	do {
		// if i isn't prime, continue
		$i = $small_primes[$loc];
		if($i == 0) die("need more small primes");


		$n = new bitplane(); // automatically fill it..
		print "filling... "; flush();
		$n->fill($i, $num_to_factor % $i);
		// each entry should be equal to (x%i * y%i) % i 0<=x<i 0<=y<i
		print "intersecting... "; flush();

		$curr = $curr->intersect($n);
		// intersect simply creates a new bitplane, iterates over all the points calling find_next_point_coord

		print "i is $i, count is ";
		print count($curr->points);
		print ", size is " . $curr->size;
		print ", $num_to_factor % $i = " . ($num_to_factor % $i);
		print ", should have checked all numbers up to " . ($curr->size);
		print " " . 100 * ($curr->size * $curr->size) / $num_to_factor . "%";
//		print_r($curr->points);
		print "\n";
		$loc++;
	} while(true);

	function test_match($p, $n) {
		if($n % $p == 0 && $p != 1) {
			print "Found match\n";
			print $p . " * " . ($n / $p) . " = $n\n";
			die();
		}
	}

	class bitplane {
		public $size = 0;

		public $points = array();

		function fill($size, $match) {
			$this->size = $size;
			for($x = 0; $x < $size; $x++) {
				for($y = 0; $y <= $x; $y++) {
					if((($x % $size) * ($y % $size)) % $size == $match) {
						$r = array();
						$r['x'] = $x;
						$r['y'] = $y;
						$this->points[] = $r;
						$r['x'] = $y;
						$r['y'] = $x;
						$this->points[] = $r;
					}
				}
			}

		}

		function add_point($r) {
			foreach($this->points as $p) {
				if($p['x'] == $r['x'] && $p['y'] == $r['y']) return;
			}
			$this->points[] = $r;
		}

		function intersect($a) {
			if($this->size == 0) return $a;

			$n = new bitplane();
			$n->size = $a->size * $this->size;

//			print "size is {$n->size}\n";

			// iterate all our points and all their points, adding them to $n
			foreach($this->points as $p) {
				foreach($a->points as $q) {
					$r = array();
					$r['x'] = find_next_point_coord($p['x'], $q['x'], $this->size, $a->size);
					$r['y'] = find_next_point_coord($p['y'], $q['y'], $this->size, $a->size);
					$n->add_point($r);
				}
//				print "end of outer loop\n";
			}

			return $n;
		}
	}
?>
