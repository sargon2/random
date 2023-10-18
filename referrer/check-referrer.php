<?
	header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
	header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
	header("Cache-Control: no-store, no-cache, must-revalidate");
	header("Cache-Control: post-check=0, pre-check=0", false);
	header("Pragma: no-cache");

	if(isset($GLOBALS['HTTP_REFERER'])) {
		print "<h2>HTTP/1.1 403 Forbidden</h2><br><h3>This site does not allow offsite or \"hot\" linking.</h3>";
		exit();
	}

	print "Normal site content!<br>";
	print "<a href=\"http://referrer.xem.us\">go back</a>";
?>
