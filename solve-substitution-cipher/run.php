<?
	$ciphertext = file_get_contents("ciphertext.txt");
	$ciphertext = strtolower($ciphertext);
	$freqs = array();
	foreach(range('a', 'z') as $l) {
		$freqs[$l] = 0;
	}
	$letters = str_split($ciphertext);
	foreach($letters as $letter) {
		if(preg_match("/[a-z]/", $letter))
			$freqs[$letter]++;
	}
	arsort($freqs);
	print_r($freqs);
	$ref = file("freqs.txt");
	$english_freqs = array();
	foreach($ref as $line) {
		$english_freqs[] = trim($line);
	}
	print_r($english_freqs);
	$lookup = array_combine(array_keys($freqs), $english_freqs);
	print_r($lookup);
	foreach($letters as $letter) {
		if(isset($lookup[$letter]))
			print $lookup[$letter];
		else
			print $letter;
	}
?>
