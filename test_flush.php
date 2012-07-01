<?
	putenv("no-gzip");
	putenv("no-deflate");
?>
<html><body>
<?
	for($i=0;$i<10;$i++) {
		print $i . "<br>\n";
		flush();
		sleep(1);
	}
?>
</body></html>
