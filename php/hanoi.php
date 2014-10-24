<?
	function solveTowers($count, $source, $destination, $spare) {
		if($count == 1) {
			print "Move top disk from pole $source to pole $destination\n";
		} else {
			solveTowers($count-1, $source, $spare, $destination);
			solveTowers(1, $source, $destination, $spare);
			solveTowers($count-1, $spare, $destination, $source);
		}
	}

	solveTowers(3, 'a', 'b', 'c');
?>
