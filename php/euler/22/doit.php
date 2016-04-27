<?
	$names = trim(file_get_contents("names.txt"));
	$names = explode(",", $names);
	sort($names);
	$pos = 0;
	$sum = 0;
	foreach($names as $name) {
		$pos++;
		$name = substr($name, 1, strlen($name)-2);
		$letters = str_split($name);
		$score = 0;
		foreach($letters as $letter) {
			$score += ord($letter) - ord('A') + 1;
		}
		$score *= $pos;
		$sum += $score;
	}
	print "sum is $sum\n";
?>
