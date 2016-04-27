<?

set_time_limit(60);

if(!isset($filename)) $filename = "alg_test.jpg";
$filename = str_replace("/", "", $filename);
$filename = str_replace("~", "", $filename);
$im = imagecreatefromjpeg($filename);
if(!$im) die("Could not load image");


$wid = imagesx($im);
$height = imagesy($im);

$im_new = imagecreatetruecolor($wid, $height);
imagecolorallocate($im_new, 0, 0, 0);

// find maximum + minimum HSV saturation/value
$max_sat = 0; $min_sat = 1;
$max_val = 0; $min_val = 1;

for($i=0;$i<$wid;$i++) {
	for($j=0;$j<$height;$j++) {
		$c = colorat($im, $i, $j);
		$hsv = rgb2hsv(array($c['red']/255, $c['green']/255, $c['blue']/255));
		list($h, $s, $v) = $hsv;

		if($s > $max_sat) $max_sat = $s;
		if($s < $min_sat) $min_sat = $s;

		if($v > $max_val) $max_val = $v;
		if($v < $min_val) $min_val = $v;
	}
}


// calculate offset and expansion factor

// if max is .5 and min is 0.. s_offset will be 0 and s_exp will be 1 / (.5 - 0) = 1 / .5 = 2
// if max is 1 and min is .5, s_offset will be -.5 and s_exp will be 1/(1-.5) = 1/.5 = 2
$s_offset = 0 - $min_sat;
$s_exp = 1 / ($max_sat - $min_sat);

$v_offset = 0 - $min_val;
$v_exp = 1 / ($max_val - $min_val);

for($i=0;$i<$wid;$i++) {
	for($j=0;$j<$height;$j++) {
		$c = colorat($im, $i, $j);
		list($h, $s, $v) = rgb2hsv(array($c['red']/255, $c['green']/255, $c['blue']/255));
		$s = ($s * $s_exp) + $s_offset;
		$s = pow($s, 0.8);
		if($s > 1) $s = 1;
		if($s < 0) $s = 0;
		$v = ($v * $v_exp) + $v_offset;
		if($v > 1) $v = 1;
		if($v < 0) $v = 0;
		list($r, $g, $b) = hsv2rgb(array($h, $s, $v));
		setpixel($im_new, $i, $j, $r*255, $g*255, $b*255);
	}
}

imagejpeg($im_new);
imagejpeg($im_new, "/tmp/delme.jpg", 80);


function setpixel($im, $x, $y, $r, $g, $b) {
	$c = imagecolorallocate($im, $r, $g, $b);
	if($c == -1) die("Invalid color?");
	imagesetpixel($im, $x, $y, $c);
	imagecolordeallocate($im, $c);
}

function colorat($im, $x, $y) {
	$c_index = imagecolorat($im, $x, $y);
	$c = imagecolorsforindex($im, $c_index);

	return $c;
}

// $c = array($red, $green, $blue)
// $red=[0..1], $green=[0..1], $blue=[0..1];
function rgb2hsv($c) {
	list($r,$g,$b)=$c;
	$v=max($r,$g,$b);
	$t=min($r,$g,$b);
	$s=($v==0)?0:($v-$t)/$v;
	if ($s==0)
		$h=-1;
	else {
		$a=$v-$t;
		$cr=($v-$r)/$a;
		$cg=($v-$g)/$a;
		$cb=($v-$b)/$a;
		$h=($r==$v)?$cb-$cg:(($g==$v)?2+$cr-$cb:(($b==$v)?$h=4+$cg-$cr:0));
		$h=60*$h;
		$h=($h<0)?$h+360:$h;
	}
	return array($h,$s,$v);
}

// $c = array($hue, $saturation, $brightness)
// $hue=[0..360], $saturation=[0..1], $brightness=[0..1]
function hsv2rgb($c) {
	list($h,$s,$v)=$c;
	if ($s==0)
		return array($v,$v,$v);
	else {
		$h=($h%=360)/60;
		$i=floor($h);
		$f=$h-$i;
		$p = $v * (1 - $s);
		$q = $v * (1 - $s * $f);
		$t = $v * (1 - $s * (1 - $f));

		switch($i) {
		case 0: return array($v, $t, $p);
		case 1: return array($q, $v, $p);
		case 2: return array($p, $v, $t);
		case 3: return array($p, $q, $v);
		case 4: return array($t, $p, $v);
		case 5: return array($v, $p, $q);
		default: die("error in alg");
		}
	}
}
