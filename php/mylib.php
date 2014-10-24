<?
	function _print_r($arg) {
		print "<pre>";
		print_r($arg);
		print "</pre>";
	}

	function chomp($data) { // Handles arrays, but still acts like other php functions in that it doesn't modify its arg
		if(is_array($data)) {
			$ret = array();
			foreach($data as $k=>$v) {
				$ret[$k] = chomp($v);
			}
			return $ret;
		} else {
			if(substr($data, strlen($data) - 1, 1) == '\n') {
				$data = substr($data, 0, -1);
			}
			return $data;
		}
	}

	function print_select($name, $options) { // option for other args to select (i.e. class=?) ?
		$setting = $_REQUEST[$name];
		print "<select name=\"$name\">";
		foreach($options as $option) {
			print "<option";
			if($setting == $option) print " selected";
			print ">$option</option>\n";
		}
		print "</select>";
	}

	function starttimer() {
		global $_starttime;
		$a = gettimeofday();
		$_starttime = $a['sec']+($a['usec']/1000000);
	}
	function getelapsed() {
		global $_starttime;
		$a = gettimeofday();
		$endtime = $a['sec']+$a['usec']/1000000;
		$val = $endtime - $_starttime;
		$val = preg_replace("/^([^.]+\.0*.{3})[^E]*(E.*)?$/", "$1$2", $val);
		return $val;
	}
	starttimer(); // if we want to override this, we can just call it again
?>
