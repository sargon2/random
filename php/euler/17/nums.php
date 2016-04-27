<?
	$nums = array();
	$nums[0] = "zero";
	$nums[1] = "one";
	$nums[2] = "two";
	$nums[3] = "three";
	$nums[4] = "four";
	$nums[5] = "five";
	$nums[6] = "six";
	$nums[7] = "seven";
	$nums[8] = "eight";
	$nums[9] = "nine";
	$nums[10] = "ten";
	$nums[11] = "eleven";
	$nums[12] = "twelve";
	$nums[13] = "thirteen";
	$nums[14] = "fourteen";
	$nums[15] = "fifteen";
	$nums[16] = "sixteen";
	$nums[17] = "seventeen";
	$nums[18] = "eighteen";
	$nums[19] = "nineteen";
	$nums[20] = "twenty";
	$nums[30] = "thirty";
	$nums[40] = "forty";
	$nums[50] = "fifty";
	$nums[60] = "sixty";
	$nums[70] = "seventy";
	$nums[80] = "eighty";
	$nums[90] = "ninety";
	$nums[1000] = "one thousand"; // hax

	function get_num($num) {
		global $nums;
		if(isset($nums[$num])) {
			return $nums[$num];
		}
		$ret = "";
		$last_two = $num % 100;
		if($last_two > 0 && isset($nums[$last_two])) $ret = $nums[$last_two];
		else {
			$num -= $last_two;
			$last = $last_two % 10;
			$last_two -= $last;
			if($last_two != 0) $ret = $nums[$last_two] . " " . $nums[$last];
			else if($last != 0) $ret = $nums[$last];
		}
		if($num != 0) {
			$num /= 100;
			if($ret == "") $ret = $nums[$num] . " hundred";
			else $ret = $nums[$num] . " hundred and " . $ret;
		}
		return $ret;
	}
?>
