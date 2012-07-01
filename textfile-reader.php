<html><body style="font-family: monospace; font-size: 14px">
<form>
url: <input type="text" name="url" value="<?=$url?>"/>
<input type="submit" />
</form>
<?
	if($url == "") die();
	if(!preg_match("/^http/", $url)) $url = "http://" . $url; // for security
	$file = file_get_contents($url);
	$file = str_replace("\n", "<br />\n", $file);
	print($file);
?>
</body></html>
