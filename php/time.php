<?
	function starttimer() {
		global $starttime;
		$a = gettimeofday();
		$starttime = $a[sec]+($a[usec]/1000000);
	}

	function getelapsed() {
		global $starttime;
        	$a = gettimeofday();
	        $endtime = $a['sec']+$a['usec']/1000000;
	        $val = $endtime - $starttime;
	        $val = preg_replace("/^([^.]+\.0*.{3}).*$/", "$1", $val);
		return $val;
	}
?>
