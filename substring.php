<?
	require_once("time.php");
	$haystack = file_get_contents("/home/sargon/log/#ro/09.13.2004.log");
	
	$needle = "asdf";

	$num = 1000;

	starttimer();
	for($i=0;$i<$num;$i++)
		strstr($haystack, $needle);
	$elapsed = getelapsed();

	print "strstr: $elapsed<br>\n";

	starttimer();
	for($i=0;$i<$num;$i++)
		preg_match("/$needle/", $haystack);
	$elapsed = getelapsed();

	print "preg_match: $elapsed<br>\n";
?>
