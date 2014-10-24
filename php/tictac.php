<?
	$letters = array("a", "b", "c", "d", "e", "f", "g", "h", "i");

//	$letters = array("a", "b", "c", "d", "e");

#	a|b|c
#	-+-+-
#	d|e|f
#	-+-+-
#	g|h|i

//	$log = array();

	recurse($letters);

	function recurse($letters, $build = "") {
		global $log;
		$result = checkforwin($build);
		if($result != 0) {
			// Log the result
			print "$build: $result\n";
			return; // no need to continue
		}
		if(count($letters) == 0) {
			print "$build: 0\n";
			return;
		}
		for($i=0;$i<count($letters);$i++) {
			$curr = $letters[$i];
			$rest = $letters;
			array_splice($rest, $i, 1);
			recurse($rest, $build . $curr);
		}
	}

	function checkforwin($build) {
		// 0 means no winner, 1 means X wins, 2 means O wins
		$lines = array("abc", "def", "ghi", "adg", "beh", "cfi", "aei", "ceg");
		if(strlen($build) < 5) return 0;

		// Because of the order we're testing in, we know that the last letter added will be part of the win line.
		// Therefore, we know who will be the winner -- we just have to test if it was a win or not.
		if(strlen($build) % 2 == 0) $winner = 2;
		else $winner = 1;

		// Take out every other element, starting with the end.  This leaves us with all the winner's moves
		for($i=strlen($build)-2;$i>=0;$i-=2) {
			$build = substr($build, 0, $i) . substr($build, $i + 1);
		}

		// Check for a valid line
		foreach($lines as $line) {
			$has = 0;
			for($i=0;$i<3;$i++) {
				$line_letter = substr($line, $i, 1);
				if(strstr($build, $line_letter) !== false) {
					$has++;
				}
			}
			if($has == 3) {
				return $winner;
			}
		}
		return 0;
	}
?>
