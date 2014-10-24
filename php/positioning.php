<?
	header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
	header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
	header("Cache-Control: no-store, no-cache, must-revalidate");
	header("Cache-Control: post-check=0, pre-check=0", false);
	header("Pragma: no-cache");
	$show_top = 100;
	$show_left = 10;
	$click_top = 150; // mt_rand(50, 500);
	$click_left = 500; // mt_rand(500, 1000);
	if(isset($coords)) {
		$vals = explode(",", $coords);
		// if we're in ie, don't do this
		if(!strstr($GLOBALS['HTTP_USER_AGENT'], "MSIE")) {
//			$myimage_x -= $click_left;
//			$myimage_y -= $click_top;
		}
//		print "x: {$vals[0]} -> $myimage_x<br>\n";
//		print "y: {$vals[1]} -> $myimage_y<br>\n";
		$xoffby = $myimage_x - $vals[0];
		$yoffby = $myimage_y - $vals[1];
		$dist = sqrt(pow($xoffby,2) + pow($yoffby,2));
//		print "dist: $dist<br>\n";
		?>
<image style="border: 1px solid black; position: absolute; top: <?=$click_top?>px; left: <?=$click_left?>px;" src="blank.gif" width="400" height="400">
<image src="black.gif" width="5" height="5" style="position: absolute; top: <?=$vals[1] + $click_top?>px; left: <?=$vals[0] + $click_left?>px;" />
<image src="black.gif" width="2" height="2" style="position: absolute; top: <?=$myimage_y + $click_top?>px; left: <?=$myimage_x + $click_left?>px;" />
		<?
	}
	$curx = mt_rand(0, 400);
	$cury = mt_rand(0, 400);
	$coords = "$curx,$cury";
	if(!isset($num)) $num = 0;
	if(!isset($tot_dist)) $tot_dist = 0;
	if(!isset($tot_x)) $tot_x = 0;
	if(!isset($tot_y)) $tot_y = 0;
	$tot_dist += $dist;
	$tot_x += $xoffby;
	$tot_y += $yoffby;
	$av = null;
	$avx = null;
	$avy = null;
	if($num > 0) {
		$av = $tot_dist / $num;
		$avx = $tot_x / $num;
		$avy = $tot_y / $num;
	}
?>
Click in the right box where the dot in the left box would be<br>
Num done: <?=$num?>, last distance: <?=$dist?> (<?=$xoffby?>, <?=$yoffby?>), average distance: <?=$av?> (<?=$avx?>, <?=$avy?>)<br>
<a href="positioning.php">Start over</a><br>
<image style="border: 1px solid black; position: absolute; top: <?=$show_top?>px; left: <?=$show_left?>px;" src="blank.gif" width="400" height="400">
<image src="black.gif" width="5" height="5" style="position: absolute; top: <?=$cury + $show_top?>px; left: <?=$curx + $show_left?>px;" />
<form method="POST">
<input style="cursor: crosshair; border: 1px solid black; position: absolute; top: <?=$click_top?>px; left: <?=$click_left?>px;" type="image" name="myimage" src="blank.gif" width="400" height="400">
<input type="hidden" name="coords" value="<?=$coords?>">
<input type="hidden" name="num" value="<?=$num+1?>">
<input type="hidden" name="tot_dist" value="<?=$tot_dist?>">
<input type="hidden" name="tot_x" value="<?=$tot_x?>">
<input type="hidden" name="tot_y" value="<?=$tot_y?>">
</form>
