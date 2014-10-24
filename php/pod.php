<?
	$day = date("d");
	$month = date("m");
	$year = date("y");

	$url = "http://lava.nationalgeographic.com/cgi-bin/pod/wallpaper.cgi?day=$day&month=$month&year=$year";

	$src = file($url);
	$found = false;
	foreach($src as $l) {
		if(preg_match("@/pod/pictures/lg_wallpaper/([^\.]+\.jpg)@", $l, $matches)) {
			$name = $matches[1];
			$found = true;
			break;
		}
	}
	if(!$found) print "Error<br>\n";
	$pic_url = "http://lava.nationalgeographic.com/pod/pictures/lg_wallpaper/" . $matches[1];
	header("Location: $pic_url");
	
?>
