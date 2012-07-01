<?
header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
header("Cache-Control: no-store, no-cache, must-revalidate");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

header("Content-type: image/png");

$N = 50;
$bw = 20;
$font = 5;

$width = $N * $bw + $N;
$height = 400;
$im = imagecreatetruecolor($width, $height);
$white = imagecolorallocate($im, 255, 255, 255);
$black = imagecolorallocate($im, 0, 0, 0);
imagefilledrectangle($im, 0, 0, $width, $height, $white);

$cp = 0;
for($i=0;$i<=$N;$i++) {
	$b = 255 - $N + $i;

	$c = imagecolorallocate($im, 255, $b, $b);
	imagefilledrectangle($im, $i * $bw, 0, ($i + 1) * $bw - 2, 100, $c);
	imagestringup($im, $font, $i * $bw + 1, 53, $i, $white);

	$c = imagecolorallocate($im, $b, 255, $b);
	imagefilledrectangle($im, $i * $bw, 100, ($i + 1) * $bw - 2, 200, $c);
	imagestringup($im, $font, $i * $bw + 1, 153, $i, $white);

	$c = imagecolorallocate($im, $b, $b, 255);
	imagefilledrectangle($im, $i * $bw, 200, ($i + 1) * $bw - 2, 300, $c);
	imagestringup($im, $font, $i * $bw + 1, 253, $i, $white);

	$c = imagecolorallocate($im, $b, $b, $b);
	imagefilledrectangle($im, $i * $bw, 300, ($i + 1) * $bw - 2, 400, $c);
	imagestringup($im, $font, $i * $bw + 1, 353, $i, $white);
}
/*
for($i=0;$i<=260;$i++) {
	$b = 230 + ($i / 10);
	$c = imagecolorallocate($im, 255, $b, $b);
	imageline($im, $i, 0, $i, 100, $c);
	imagestringup($im, 1, $i * 10 + 1, 50, $i, $c);
	$c = imagecolorallocate($im, $b, 255, $b);
	imageline($im, $i, 101, $i, 200, $c);
	$c = imagecolorallocate($im, $b, $b, 255);
	imageline($im, $i, 201, $i, 300, $c);
	$c = imagecolorallocate($im, $b, $b, $b);
	imageline($im, $i, 301, $i, 400, $c);
}
*/

imagepng($im);
?>
