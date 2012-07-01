<?
	if(!isset($shades)) $shades = 128;

	if($shades > 255) die("Shades must be 255 or less");
	if($shades < 2) die("Shades must be 2 or larger");
	$im = imagecreatetruecolor(255,100);
	for($i=0;$i<=255;$i++) {
		$l = ($i * $shades) / 255;
		$l = (int) $l;
		$l = ($l * 255) / $shades;
		$l = (int) $l;
		$c = imagecolorallocate($im, $l, $l, $l);
		imageline($im, $i, 0, $i, 100, $c);
	}

	imagepng($im);

?>
