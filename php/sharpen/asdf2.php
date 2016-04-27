<?

	$url = "http://davidbesen.com/shoebox/thumbs/pics/2004-06-12-basc%20cat/IMG_3568.JPG";

	$im = imagecreatefromstring(file_get_contents($url));

	// SETTINGS
	$passes = 3; // integer >= 1, basically the radius of the change
	$delta = 0.1; // float 0-1, how much difference to make
	$threshhold1 = .6; // float 0-1, how much contrast a block has to have before we won't change it.. to try to help antialiasing
	$threshhold2 = 0.02; // float 0-1, how close values are before we don't change them (to maintain detail)
	//

	for($i=0;$i<$passes;$i++) {
		$cache = array();
		$im = pass($im);
	}

	imagejpeg($im, "test2.jpg", 95);

	function pass($im) {
		$x = imagesx($im);
		$y = imagesy($im);
		$im2 = imagecreatetruecolor($x, $y);

		for($i = 0;$i<$x;$i++) {
			for($j=0;$j<$y;$j++) {
				$rgb = getvals(get9($im, $i, $j));

				$color = imagecolorallocate($im2, $rgb[0], $rgb[1], $rgb[2]);
				imagesetpixel($im2, $i, $j, $color);
				imagecolordeallocate($im2, $color);
			}
			if($i % 10 == 0) print "i is $i\n";
		}
		return $im2;
	}

	

	function get9($im, $x, $y) { // to make it easy to average, min, max, etc

		$radius = 1;

		global $cache;
		$ret = array();
		for($i = $x-$radius; $i <= $x+$radius; $i++) {
			for($j = $y-$radius; $j <= $y+$radius; $j++) {
				if(!isset($cache[$i][$j])) {
					$c = imagecolorat($im, $i, $j);
					$c = imagecolorsforindex($im, $c);
					$cache[$i][$j] = rgb2hsv($c['red'], $c['green'], $c['blue']);
				}

				if($i == $x && $j == $y) {
					$ret['curr'] = $cache[$i][$j];
				} else {
					$ret[] = $cache[$i][$j];
				}
	
			}
		}

		return $ret;
	}

	function getvals($colors) {
		global $threshhold1;
		$a = 0;
		$curr = "";
		foreach($colors as $k=>$c) {
			$a += $c[2];

			if($k == 'curr') $curr = $c;
		}
		$a /= count($colors);
		$maxv = maxv($colors);
		$minv = minv($colors);

		if(($maxv - $minv) > $threshhold1) return hsv2rgb($curr[0], $curr[1], $curr[2]);

		if($curr[2] >= $a) {
			$rgb = hsv2rgb($curr[0], $curr[1], mergev($curr[2], maxv($colors)));
			return $rgb;
		}
		$rgb = hsv2rgb($curr[0], $curr[1], mergev($curr[2], minv($colors)));
		return $rgb;
	}

	function maxv($colors) {
		$v = 0;
		foreach($colors as $c) {
			if($v < $c[2]) $v = $c[2];
		}

		return $v;
	}

	function minv($colors) {
		$v = 1;
		foreach($colors as $c) {
			if($v > $c[2]) $v = $c[2];
		}

		return $v;
	}

	function mergev($v, $maxv) {
		global $delta;
		global $threshhold2;

		$diff = $maxv - $v;

		if(abs($diff) < $threshhold2) return $v;

		$diff *= $delta;
		return $v + $diff;
	}

function hsv2rgb($h, $s, $v) {
    
        # Adapted from C source code found here:
        # http://www.cs.rit.edu/~ncs/color/t_convert.html
    
        if ($s == 0) {        # achromatic
            $r = $g = $b = $v;
            return array($r * 255, $g * 255, $b * 255);
        }

        $h %= 360;

        $h /= 60;
        $i = floor($h);
        $f = $h - $i;
        $p = $v * (1 - $s);
        $q = $v * (1 - $s * $f);
        $t = $v * (1 - $s * (1 - $f));
    
        switch($i) {
            case 0:
                $r = $v;
                $g = $t;
                $b = $p;
                break;
            case 1:
                $r = $q;
                $g = $v;
                $b = $p;
                break;
            case 2:
                $r = $p;
                $g = $v;
                $b = $t;
                break;
            case 3:
                $r = $p;
                $g = $q;
                $b = $v;
                break;
            case 4:
                $r = $t;
                $g = $p;
                $b = $v;
                break;
            default:        # and case 5:
                $r = $v;
                $g = $p;
                $b = $q;
                break;
        }
    
        return array($r * 255, $g * 255, $b * 255);
    
    
    }
    
    
    function rgb2hsv($red, $green, $blue) {
    
        # Adapted from C source code found here:
        # http://www.cs.rit.edu/~ncs/color/t_convert.html
    
    
        # Need values from 0 - 1 instead of 0 - 255
        #
        $r = $red   / 255;
        $g = $green / 255;
        $b = $blue  / 255;
    
        $min = min($r, $g, $b);    
        $max = max($r, $g, $b);    
    
        $v = $max;
    
        $delta = $max - $min;
    
        if ($max != 0) {
            $s = $delta / $max;
        } else {
            $s = 0;
            $h = -1;
            return array($h, $s, $v);
        }
    
    
        if ($delta) {
    
            if ($r == $max) {
                $h = ($g - $b) / $delta;
            } else if ($g == $max) {
                $h = 2 + ($b - $r) / $delta;
            } else {
                $h = 4 + ($r - $g) / $delta;
            }
    
        } else {
            $h = 0;
        }
    
        $h *= 60;
    
        if ($h < 0) {
            $h += 360;
        }
    
        return array($h, $s, $v);
    
    }

?>
