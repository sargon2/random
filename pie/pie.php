<?
	// pie.php - Draw an antialiased pie chart, either automatically or fully customized
	// All math is in degrees, not radians.
	function DrawPie($data, $xsize = null, $highlighted = null, $height = null, $viewangle = null, $aliasaccuracy = null) {
		// set up defaults..
		if($xsize == null) $xsize = 150; // in pixels
		// $highlighted is the name of a slice.  It indicates that we should rotate the graph and explode that slice.
		if($height == null) $height = 4; // also in pixels
		if($viewangle == null) $viewangle = 0.5; // not actually an angle.  1 is top-down, 0 is fuly horizontal.
		if($aliasaccuracy == null) $aliasaccuracy = 4; // integer >= 1, smaller is faster and larger is more accurate

		$data = preprocess($data);


		// Calculate y-size of the _graph_, not the image (different because of $height and $highlighted)
		$ysize = ($xsize * $viewangle);

		// Total number of slices
		$num = count($data);

		// The larger this number, the longer it takes to render.. however, we can assume that
		// the larger the graph, the more important it is on the page.
		$renderxsize = $xsize * $aliasaccuracy;
		$renderysize = $ysize * $aliasaccuracy;

		// Center of the TOP of the graph.
		$cx = $renderxsize/2;
		$cy = $renderysize/2;

		// Compensate $height for the resampling
		$renderheight = $height * $aliasaccuracy;

		$outputim = imagecreatetruecolor($xsize, $ysize + $height);
		$renderim = imagecreatetruecolor($renderxsize+1, $renderysize+$renderheight+1);

		// Set up our colors
		$colors = GetColors($renderim, $num);
		$white = imagecolorallocate($renderim, 255, 255, 255);
		$black = imagecolorallocate($renderim, 0, 0, 0);
		$grey = imagecolorallocate($renderim, 128, 128, 128);

		// Compensate drawing width for our downsampling
		imagesetthickness($renderim, $aliasaccuracy);

		// Fill the background
		imagefilledrectangle($renderim, 0, 0, $renderxsize+1, $renderysize + $renderheight+1, $white);

		$angleoffset = 0;

		// Calculate the angles for each slice.
		$sum = 0;
		$angles = array();
		foreach($data as $record) $sum += $record;
		$rsum = 0;
		foreach($data as $k=>$record) {
			$rsum += $record;
			$angle = ($rsum * 360) / $sum;
			if($k == $highlighted) $angleoffset = $angle;
			$angles[] = $angle;
		}

		$angleoffset -= 430;

		// Draw the base of the pie chart
		imagefilledarc($renderim, $cx, $cy + $renderheight, $renderxsize, $renderysize, 0, 360, $grey, IMG_ARC_PIE);

		// black outline -- have to compensate size of image for this..
//		imagefilledarc($renderim, $cx, $cy, $renderxsize + $aliasaccuracy*2, $renderysize + $aliasaccuracy*2, 0, 360, $black, IMG_ARC_PIE);

		// Draw the top of the pie chart.  This should be last.
		$prevangle = 0;
		for($i=0;$i<$num;$i++) {
			$angle = $angles[$i];
			imagefilledarc($renderim, $cx, $cy, $renderxsize, $renderysize, $prevangle - $angleoffset, $angle - $angleoffset, $colors[$i], IMG_ARC_PIE);
			$prevangle = $angle;
		}

		imagearc($renderim, $cx, $cy, $renderxsize, $renderysize, 0, 359, $black);

		// Perform the resampling.
		imagecopyresampled($outputim, $renderim, 0, 0, 0, 0, $xsize, $ysize+$height, $renderxsize, $renderysize+$renderheight);

		// Output the image
		if(headers_sent()) die("\nHeaders already sent.\n");
		header("Content-type: image/png");
		imagepng($outputim);
	}

	function preprocess($data) {
		arsort($data);

		// Combine all values in the smallest 10% into one "Other" value?

		return $data;
	}

	function GetEndpoint($startpoint, $r, $theta, $viewangle) {
		// Math to assist in drawing each slice more accurately
	}

	function GetColors($im, $num) {
		$s = 0.75; $v = 0.95;

		$val = array();
		$index = 0;
		$cycle = 0;
		for($i=0;$i<$num;$i++) {
			$h = (($i * 0.9) / $num);

			$color = hsv2rgb($h, $s, $v);
			$val[$index] = imagecolorallocate($im, $color['red'], $color['green'], $color['blue']);
			$index += 3;
			if($index >= $num) {
				$cycle++;
				$index = $cycle;
			}
		}

		return $val;
	}

	function hsv2rgb($h, $s, $v) { // takes in 0..1, returns 0..255
		if($s == 0) {
			$r = $v * 255;
			$g = $v * 255;
			$b = $v * 255;
		} else {
			$var_h = $h * 6;
			$var_i = floor($var_h);
			$var_1 = $v * (1 - $s);
			$var_2 = $v * (1 - $s * ($var_h - $var_i));
			$var_3 = $v * (1 - $s * (1 - ($var_h - $var_i)));

			switch($var_i) {
			case 0:
				$var_r = $v; $var_g = $var_3; $var_b = $var_1;
				break;
			case 1:
				$var_r = $var_2; $var_g = $v; $var_b = $var_1;
				break;
			case 2:
				$var_r = $var_1; $var_g = $v; $var_b = $var_3;
				break;
			case 3:
				$var_r = $var_1; $var_g = $var_2; $var_b = $v;
				break;
			case 4:
				$var_r = $var_3; $var_g = $var_1; $var_b = $v;
				break;
			default:
				$var_r = $v; $var_g = $var_1; $var_b = $var_2;
				break;
			}
		}
		$ret['red'] = $var_r * 255;
		$ret['green'] = $var_g * 255;
		$ret['blue'] = $var_b * 255;
		return $ret;
	}

	$data = array();
	for($i=0;$i<7;$i++) {
		$data[] = mt_rand(0,100);
//		$data[] = $i;
	}
?>
