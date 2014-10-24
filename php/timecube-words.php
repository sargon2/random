<?
	$data = strip_tags(file_get_contents("http://www.timecube.com"));
	$data = preg_replace("/[\r\n]+/", " ", $data);
	preg_match_all("/\w+/", $data, $matches);
	$ret = array();
	foreach($matches[0] as $v) {
		$v = strtolower($v);
		if($v == "nbsp") continue;
		$ret[$v]++;
	}
	arsort($ret);
	print "<pre>";
	print_r($ret);
	print "</pre>";
?>
