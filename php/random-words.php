<?
$file = file("/usr/share/dict/words");
//$file = preg_grep("/^[a-z]{1,4}$/", $file);
usort($file, "cmp");
$file = array_slice($file, 0, 30);
foreach($file as $word) print "$word<br>";
function cmp($a, $b) { return mt_rand(0,1) >0.5 ? 1 : -1; }
?>
