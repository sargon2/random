<?
	require_once("nums.php");
	for($i=1;$i<=1000;$i++) {
		$s = get_num($i);
		$s = str_replace(" ", "", $s);
		$count += strlen($s);
		print $s . "\n";
	}
	print $count;
?>
