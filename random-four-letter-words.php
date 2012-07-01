<?
$file = file("/usr/share/dict/words");
$file = preg_grep("/^[a-z]{1,4}$/", $file);
	usort($file, "cmp");
	foreach($file as $word) print "$word ";
	function cmp($a, $b) { return mt_rand(0,1) >0.5 ? 1 : -1; }
?>
