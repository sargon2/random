<?
	header("Content-type: image/gif");
	$height = 1000;
	$width = 1000;
	$step = 100;
	$im = imagecreatetruecolor($width+1, $height+1);
	imageantialias($im, true);
	$white = imagecolorallocate($im, 255, 255, 255);
	$gray = imagecolorallocate($im, 100, 100, 100);
	$ltgray = imagecolorallocate($im, 200, 200, 200);
	$black = imagecolorallocate($im, 0, 0, 0);

	imagefilledrectangle($im, 0, 0, $width, $height, $white);

	for($i=0;$i<=$width;$i+=$step) {
		imageline($im, $i, 0, $i, $height, $ltgray);
	}

	for($i=0;$i<=$height;$i+=$step) {
		imageline($im, 0, $i, $height, $i, $ltgray);
	}

	draw_star(-100, -100);
	draw_star(1100, -100);
	draw_star(500, 1100);

	imagegif($im);

	function draw_star($cx, $cy) {
		global $im, $gray, $width, $height, $step;
		for($i=0;$i<=$width;$i+=$step) {
			imageline($im, $cx, $cy, $i, 0, $gray);
			imageline($im, $cx, $cy, $i, $height, $gray);
		}
		for($i=0;$i<=$height;$i+=$step) {
			imageline($im, $cx, $cy, 0, $i, $gray);
			imageline($im, $cx, $cy, $width, $i, $gray);
		}
	}
?>
