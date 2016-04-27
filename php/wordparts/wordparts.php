<?
	$fp = fopen("/etc/dictionaries-common/words", "r");
	$single_letters = array();
	$twoletters = array();
	$twoletters_beginning = array();
	$twoletters_end = array();
	$threeletters = array();
	$threeletters_beginning = array();
	$threeletters_end = array();
	while(!feof($fp)) {
		$line = fgets($fp);
		$line = trim($line);
		if(preg_match("/'s$/", $line)) continue;
		if(strlen($line) < 4) continue;
		if(strlen($line) > 7) continue;
		if(preg_match("/[A-Z]/", $line)) continue;
		if(preg_match("/^[a-z]+$/", $line)) process($line);
	}

	// do sorting
	arsort($single_letters);
	arsort($twoletters);
	arsort($twoletters_beginning);
	arsort($twoletters_end);
	arsort($threeletters);
	arsort($threeletters_beginning);
	arsort($threeletters_end);

	print "Single letters: "; printit($single_letters);
	print "Two-letter combos: "; printit($twoletters);
	print "Two-letter combos (beginning): "; printit($twoletters_beginning);
	print "Two-letter combos (end): "; printit($twoletters_end);
	print "Three-letter combos: "; printit($threeletters);
	print "Three-letter combos (beginning): "; printit($threeletters_beginning);
	print "Three-letter combos (end): "; printit($threeletters_end);

	function printit($thing) {
		$thing = array_slice($thing, 0, 10);
		$keys = array_keys($thing);
		print join(" ", $keys);
		print "\n";
	}

	function process($word) {
		global $single_letters;
		global $twoletters;
		global $twoletters_beginning;
		global $twoletters_end;
		global $threeletters;
		global $threeletters_beginning;
		global $threeletters_end;

		for($i=0;$i<strlen($word);$i++) {
			$single_letters[$word[$i]]++;
		}

		for($i=0;$i<strlen($word)-1;$i++) {
			$part = $word[$i] . $word[$i+1];
			$twoletters[$part]++;
			if($i == 0) $twoletters_beginning[$part]++;
			if($i == strlen($word)-2) $twoletters_end[$part]++;
		}
		for($i=0;$i<strlen($word)-2;$i++) {
			$part = $word[$i] . $word[$i+1] . $word[$i+2];
			$threeletters[$part]++;
			if($i == 0) $threeletters_beginning[$part]++;
			if($i == strlen($word)-3) $threeletters_end[$part]++;
		}
	}
?>
