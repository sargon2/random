<?
	$imagewidth = 250;
	$imageheight = 200;

	$im = imagecreatetruecolor($imagewidth, $imageheight);
	$white = imagecolorallocate($im, 255, 255, 255);
	$black = imagecolorallocate($im, 0, 0, 0);
	imagefilledrectangle($im, 0, 0, $imagewidth, $imageheight, $white);

	$minre = -2;
	$maxre = 1;
	$minim = -1.2;
	$maxim = $minim + ($maxre-$minre)*$imageheight/$imagewidth;
	$re_factor = ($maxre-$minre)/($imagewidth-1);
	$im_factor = ($maxim-$minim)/($imageheight-1);
	$maxiterations = 30;

	for($y=0;$y<$imageheight;$y++) {
		$c_im = $maxim - $y*$im_factor;
		for($x=0;$x<$imagewidth;$x++) {
			$c_re = $minre + $x*$re_factor;
			$z_re = $c_re;
			$z_im = $c_im;
//			$isinside = true;
			for($n=0;$n<$maxiterations;$n++) {
				$z_re2 = $z_re*$z_re;
				$z_im2 = $z_im*$z_im;
				if($z_re2 + $z_im2 > 4) {
//					$isinside = false;
					break;
				}
				$z_im = 2*$z_re*$z_im + $c_im;
				$z_re = $z_re2 - $z_im2 + $c_re;
			}
//			if($isinside) {
//				imagesetpixel($im, $x, $y, $black);
//			} else {
				$r = 255 - (255 * $n / $maxiterations);
				$c = imagecolorallocate($im, $r, $r, $r);
				imagesetpixel($im, $x, $y, $c);
//				imagecolordeallocate($im, $c);
//			}
		}
	}

	header("Content-type: image/png");
	imagepng($im);


?>
