<?
header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
header("Expires: Mon, 26 Jul 1997 05:00:00 GMT"); // Date in the past
?>
<html>
<head>
<style><!--
table {border-collapse: collapse; }
td,th { border: 1px solid black; }
--></style>
<body>
<?
	if(!isset($num_per_row)) $num_per_row = 50;
	if(!isset($num)) $num = 50;
	?><form method="GET">
	Num rolls per row: <input type="text" name="num_per_row" value="<?=$num_per_row?>"><br>
	Num rows: <input type="text" name="num" value="<?=$num?>"><br>
	<input type="submit"><br><br>
	<?
	$none_count = 0;
	print "<table>";
	print "<tr>";
	for($i=2;$i<=12;$i++) {
		print "<th>$i</th>";
	}
	print "<th>Anomaly</th>";
	print "</tr>";
	for($j=0;$j<$num;$j++) {
		print "<tr>";
		$res = roll_dice(2, $num_per_row);
		if($num_per_row > 20) $find_zeros = true;
		else $find_zeros = false;
		$anom = find_anomaly_2($res, $find_zeros);
		if($anom == "None") $none_count++;
		for($i=2;$i<=12;$i++) {
			$r = $res[$i];
			if($r == "") $r = "0";
			print "<td>" . $r . "</td>";
		}
		print "<td>$anom</td>";
		print "</tr>";
	}
	print "</table><br>";
	$p = $none_count / $num;
	$p *= 100;
	print $none_count . " nones ($p%)";
	function find_anomaly_2($rolls, $find_zeros = true) {
		$ret = "";
		if($rolls[2] > $rolls[3] ||
		$rolls[3] > $rolls[4] ||
		$rolls[4] > $rolls[5] ||
		$rolls[5] > $rolls[6] ||
		$rolls[6] > $rolls[7] ||
		$rolls[7] < $rolls[8] ||
		$rolls[8] < $rolls[9] ||
		$rolls[9] < $rolls[10] ||
		$rolls[10] < $rolls[11] ||
		$rolls[11] < $rolls[12]) {
			$ret .= "not strictly inc/decreasing, ";
		}
		for($i=2;$i<=12;$i++) {
			if($rolls[$i] > $rolls[7]) {
				if($i >= 6 && $i <= 8) continue;
				$amount = $rolls[$i] - $rolls[7];
				if($amount == 1)
				$ret .= "$amount more roll of $i than of 7, ";
				else $ret .= "$amount more rolls of $i than of 7, ";
			}
		}
		if($find_zeros) {
			for($i=2;$i<=12;$i++) {
				if($rolls[$i] == 0) {
					$ret .= "zero rolls of $i, ";
				}
			}
		}
		if($ret == "") return "None";
		return substr($ret, 0, strlen($ret)-2);
	}
	function roll_dice($num_dice, $num_times) {
		$ret = array();
		for($j=0;$j<$num_times;$j++) {
			for($i=0;$i<$num_dice;$i++) {
				$result = 0;
				for($k=0;$k<$num_dice;$k++) {
					$result += (int) mt_rand(1, 6);
				}
				$ret[$result]++;
			}
		}
//		ksort($ret);
		return $ret;
	}
?>
</body>
</html>
