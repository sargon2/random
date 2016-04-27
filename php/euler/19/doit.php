<?
	$day = 1; // monday
	$count = 0;
	for($i=1900;$i<=2000;$i++) {
		for($month=1;$month<=12;$month++) {
			$days = get_days($month, $i);
			$day += $days;
			$day %= 7;
			if($i > 1900 && $day == 0) $count++;
		}
	}
	print "count is $count\n";
	function get_days($month, $year) {
		switch($month) {
			case 9:
			case 4:
			case 6:
			case 11:
				return 30;
			case 1:
			case 3:
			case 5:
			case 7:
			case 8:
			case 10:
			case 12:
				return 31;
			case 2:
				if(is_leap_year($year)) return 29;
				return 28;
			default:
				return -928347592875;
		}
	}
	function is_leap_year($year) {
		if($year % 4 != 0) return false;
		if($year % 400 == 0) return true;
		if($year % 100 == 0) return false;
		return true;
	}
?>
