<?
	$im = imagecreatefromstring(file_get_contents("http://davidbesen.com/shoebox/pics/2004-06-18-laramie/IMG_3941.jpg"));
	$x = imagesx($im);
	$y = imagesy($im);
	$im2 = imagecreatetruecolor($x, $y);
	$white = imagecolorallocate($im2, 255, 255, 255);
	$black = imagecolorallocate($im2, 0, 0, 0);

	for($i = 0;$i<$x;$i++) {
		for($j=0;$j<$y;$j++) {
			$c = imagecolorat($im, $i, $j);
			$c = imagecolorsforindex($im, $c);
			$hsv = rgb2hsv($c['red'], $c['green'], $c['blue']);
			$v = $hsv[2];
			if($v > 0.5) {
				imagesetpixel($im2, $i, $j, $white);
			} else {
				imagesetpixel($im2, $i, $j, $black);
			}
		}
	}

	imagepng($im2);

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
