<?
	header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
	header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
	header("Cache-Control: no-store, no-cache, must-revalidate");
	header("Cache-Control: post-check=0, pre-check=0", false);
	header("Pragma: no-cache");

	set_time_limit(60 * 5);

	if(!isset($image)) {
		print "<form>image url: <input name=\"image\" type=\"text\"><input type=\"submit\" value=\"histogram\">";
		exit();
	}

	if(!isset($mode)) $mode = "html";

	if($mode == "draw") {


		$image = imagecreatefromstring(file_get_contents($image));

		$width = imagesx($image);
		$height = imagesy($image);

		$lumdata = array();
		$rdata = array();
		$gdata = array();
		$bdata = array();

//		$max = 0;

//		$numpixels = $width * $height;

		$xstep = floor(max($width / 256, 1));
		$ystep = floor(max($height / 256, 1));
//		$tot = 0;
		for($x=0;$x<$width;$x+=$xstep) {
			for($y=0;$y<$height;$y+=$ystep) {
				$color_index = imagecolorat($image, $x, $y);
				$c = imagecolorsforindex($image, $color_index);

				$lum = floor(($c['red'] + $c['green'] + $c['blue']) / 3);

//				if($lumdata[$lum] > ($numpixels / 256) ) continue;
//				if($rdata[$c['red']] > ($numpixels / 256) ) continue;
//				if($gdata[$c['green']] > ($numpixels / 256) ) continue;
//				if($bdata[$c['blue']] > ($numpixels / 256) ) continue;
				$lumdata[$lum]++;
				$rdata[$c['red']]++;
				$gdata[$c['green']]++;
				$bdata[$c['blue']]++;
//				$tot += $c['red'] + $c['green'] + $c['blue'];
//				$max = max($lumdata[$lum], $rdata[$c['red']], $gdata[$c['green']], $bdata[$c['blue']], $max);
			}
		}

		$tmp = array_merge($lumdata,$rdata,$gdata,$bdata);
		rsort($tmp);
		$max = $tmp[6 * 4];

//		$max = $tot / (25600 * .5);
//		$max = (($tot / (255 * 3)) / $numpixels) * $max;

		// Normalize to 100 tall
		for($k=0;$k<=255;$k++) {
			$lumdata[$k] /= ($max / 100);
			$rdata[$k] /= ($max / 100);
			$gdata[$k] /= ($max / 100);
			$bdata[$k] /= ($max / 100);
		}

		$hist = imagecreatetruecolor(256, 110 * 4);
		$white = imagecolorallocate($hist, 255, 255, 255);
		imagefilledrectangle($hist, 0,0,256,110 * 4, $white);
		$black = imagecolorallocate($hist, 0, 0, 0);
		$red = imagecolorallocate($hist, 255, 0, 0);
		$green = imagecolorallocate($hist, 0, 255, 0);
		$blue = imagecolorallocate($hist, 0, 0, 255);

		$offset = 0;
		foreach(array("l", "r", "g", "b") as $color) {

			switch($color) {
			case "l": $c = $black; $tmp = $lumdata; break;
			case "r": $c = $red; $tmp = $rdata; break;
			case "g": $c = $green; $tmp = $gdata; break;
			case "b": $c = $blue; $tmp = $bdata; break;
			}

			for($x=0;$x<=255;$x++) {
				$tmp[$x] = min($tmp[$x],98);
				imageline($hist, $x, 100 + $offset, $x, $offset + (100 - $tmp[$x]), $c);
			}

			for($x=0;$x<=255;$x++) {
				switch($color) {
				case "l": $c = imagecolorallocate($hist, $x, $x, $x); break;
				case "r": $c = imagecolorallocate($hist, $x, 0, 0); break;
				case "g": $c = imagecolorallocate($hist, 0, $x, 0); break;
				case "b": $c = imagecolorallocate($hist, 0, 0, $x); break;
				}

				imageline($hist, $x, $offset + 102, $x, $offset + 110, $c);
			}

			$offset += 110;
		}

		header("Content-type: image/png");
		imagepng($hist);
	} else {
		print "<form>image url: <input name=\"image\" type=\"text\"><input type=\"submit\" value=\"histogram\"><br>";
//		if(isset($histtype)) print "Unknown variable 'histtype'<br>";
		print "<img width=\"256\" height=\"440\" src=\"?image=$image&mode=draw\"><br>";
		print "<br><img src=\"$image\">";
	}

?>
