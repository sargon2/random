<html>
<body>
<?
	if(!isset($d1)) $d1 = array(1 => 10, 10, 10, 10, 10, 10);
	if(!isset($d2)) $d2 = array(1 => 10, 10, 10, 10, 10, 10);
?>
<form>
Die 1 biases (&gt;=0, 0 means never rolled):
<table><tr><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th></tr><tr>
<td><input type="text" size="3" name="d1[1]" value="<?=$d1[1]?>"></td>
<td><input type="text" size="3" name="d1[2]" value="<?=$d1[2]?>"></td>
<td><input type="text" size="3" name="d1[3]" value="<?=$d1[3]?>"></td>
<td><input type="text" size="3" name="d1[4]" value="<?=$d1[4]?>"></td>
<td><input type="text" size="3" name="d1[5]" value="<?=$d1[5]?>"></td>
<td><input type="text" size="3" name="d1[6]" value="<?=$d1[6]?>"></td>
</tr></table>
<br>
Die 2 biases:
<table><tr><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th></tr><tr>
<td><input type="text" size="3" name="d2[1]" value="<?=$d2[1]?>"></td>
<td><input type="text" size="3" name="d2[2]" value="<?=$d2[2]?>"></td>
<td><input type="text" size="3" name="d2[3]" value="<?=$d2[3]?>"></td>
<td><input type="text" size="3" name="d2[4]" value="<?=$d2[4]?>"></td>
<td><input type="text" size="3" name="d2[5]" value="<?=$d2[5]?>"></td>
<td><input type="text" size="3" name="d2[6]" value="<?=$d2[6]?>"></td>
</tr></table>
<br>
<input type="submit">
</form>
<?
	$d1 = normalize($d1);
	$d2 = normalize($d2);
	$res = array();
	for($i=1;$i<=6;$i++) {
		for($j=1;$j<=6;$j++) {
			$res[$i + $j] += $d1[$i] * $d2[$j];
		}
	}

	function normalize($d) {
		$tot = array_sum($d);
//		if($tot == 0) return array(1 => 1/6,1/6,1/6,1/6,1/6,1/6);
		for($i=1;$i<=6;$i++) {
			if($d[$i] < 0) die("Only positive integers");
			$d[$i] = ($d[$i] / $tot);
		}
		return $d;
	}
?>
<br>
Resulting distribution:
<table><tr><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th><th>12</th></tr><tr>
<td><input type="text" size="3" value="<?=$res[2]?>"></td>
<td><input type="text" size="3" value="<?=$res[3]?>"></td>
<td><input type="text" size="3" value="<?=$res[4]?>"></td>
<td><input type="text" size="3" value="<?=$res[5]?>"></td>
<td><input type="text" size="3" value="<?=$res[6]?>"></td>
<td><input type="text" size="3" value="<?=$res[7]?>"></td>
<td><input type="text" size="3" value="<?=$res[8]?>"></td>
<td><input type="text" size="3" value="<?=$res[9]?>"></td>
<td><input type="text" size="3" value="<?=$res[10]?>"></td>
<td><input type="text" size="3" value="<?=$res[11]?>"></td>
<td><input type="text" size="3" value="<?=$res[12]?>"></td>
</tr></table>
<?
	foreach($res as $k=>$v) {
		$res[$k] = $v * 100;
	}
	$datay = implode(",", $res);
?>
	<img src="http://random.xem.us/dice-bias-graph.php?datay=<?=$datay?>">
</body></html>
