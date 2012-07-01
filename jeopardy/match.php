<?
	function guess_is_right($guess, $answer) {
		$oguess = $guess;
		$oanswer = $answer;

		$guess = strtolower($guess);
		$answer = strtolower($answer);

		// strip leading /g
		$guess = preg_replace('/^(\/g *)+/', "", $guess);

		// remove irrelevant characters
		$guess = preg_replace("/[^a-z0-9 ]/i", "", $guess);
		$answer = preg_replace("/[^a-z0-9 ]/i", "", $answer);

		// remove common leading words
		$guess = preg_replace("/^(a|mt|mount|the|an|to?)( +?)/i", "", $guess);
		$answer = preg_replace("/^(a|mt|mount|the|an|to?)( +?)/i", "", $answer);

		$guess = str_replace(" the ", " ", $guess);
		$answer = str_replace(" the ", " ", $answer);

		$guess = str_replace(" and ", "", $guess);
		$answer = str_replace(" and ", "", $answer);

		// hack so next doesn't break " s "
		$guess = str_replace(" s ", " $ ", $guess);
		$answer = str_replace(" s ", " $ ", $answer);

		// deal with plurality
		$guess = preg_replace("/s( |$)/i", " ", $guess);
		$answer = preg_replace("/s( |$)/i", " ", $answer);

		// hack so previous doesn't break " s "
		$guess = str_replace(" $ ", " s ", $guess);
		$answer = str_replace(" $ ", " s ", $answer);

		$guess = trim($guess);
		$answer = trim($answer);

		$guess_words = preg_split("/\s+/", $guess);
		$answer_words = preg_split("/\s+/", $answer);
		if(count($guess_words) != count($answer_words)) {
			// make spaces not matter
			$guess = preg_replace("/[^a-z0-9]/i", "", $guess);
			$answer = preg_replace("/[^a-z0-9]/i", "", $answer);

			if(strcasecmp($guess, $answer) == 0) return true;
			return false;
		}

		// now, we know that the # of words is the same, so we compare word by word w/ levenshtein (to avoid typos)
		foreach($guess_words as $k=>$word) {
			$aword = $answer_words[$k];
			if(levenshtein($word, $aword) > floor(strlen($aword) / 5)) return false;
		}

		return true;

	}
?>
