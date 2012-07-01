<?
	if($text) $text = stripslashes($text);
?>
<form>
<textarea name="text" cols=80 rows=25><?=$text?></textarea><br>
<input type="submit">
</form>
<?
	$text or die;
	$text = preg_replace("/\b(\w)(\w*)(\w)\b/", "$3$2$1", $text);
//	$text = preg_replace("/\s+/", "", $text);
	print $text;
?>
