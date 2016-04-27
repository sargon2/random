<?
	$file = file("data.txt");
	$data = array();
	foreach($file as $line) {
		$line = trim($line);
		$data[] = explode(" ", $line);
	}
	//print_r($data);
	print get_max($data, 0, 0);
	function get_max($data, $row, $col) {
		if(!isset($data[$row][$col])) return 0;
		$ret = $data[$row][$col] + max(get_max($data, $row+1, $col), get_max($data, $row+1, $col+1));
		//print "row $row, col $col, max $ret\n";
		return $ret;
	}
?>
