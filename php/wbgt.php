<?
	if(!isset($f)) $f = 95;
	if(!isset($rh)) $rh = 25;
?>
<form>
Wet Bulb Globe Temperature estimator:<br>
Temp (F): <input type="text" name="f" value="<?=$f?>"><br>
Relative humidity (%): <input type="text" name="rh" value="<?=$rh?>"><br>
<input type="submit" value="submit">
</form>
<?
	$ta = (5/9) * ($f-32);
	$e = $rh / 100 * 6.105 * exp(17.27 * $ta / (237.7 + $ta));
	$wbgt = 0.567 * $ta + 0.393 * $e + 3.94;

	$wbgtf = (9/5)*$wbgt+32;

	print "wbgt (F) is $wbgtf degrees";
?>
