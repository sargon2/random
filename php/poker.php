<html><head>
<style><!--
* { font-family: monospace; font-size: 10pt}
table {border-collapse: collapse; margin-left: 40px}
td {border: 1px solid black; width: 60px; text-align: center;}
th {width: 40px; }
//-->
</style></head>
<body bgcolor="white">
Initial hand win odds<br>
Green means stay in, red means fold<br>
Source: http://www.texasholdempoker-stats.com/thp_ranks.html<br>
<br><br>
<?
	// General rule of thumb, ignoring number of opponents:
	// If your hand is suited, stay in if your lowest card is a 7 or higher
	// If your hand is not suited, stay in if your lowest card is a 9 or you have a pair (except 22 or 33).

	$green_offset_val = 5; // how different the green is from white
	$red_offset_val = 2; // how different the red is from white
	$file = file("poker.txt");
	$sums = array();
	$max = array();
	$min = array();
	foreach($file as $line) {
		$fields = explode("\t", trim($line));
		for($i=1;$i<=9;$i++) {
			$sums[$i] += $fields[$i] / 169;
			if($max[$i] < $fields[$i]) $max[$i] = $fields[$i];
			if(!isset($min[$i]) || $min[$i] > $fields[$i]) $min[$i] = $fields[$i];
		}
	}

	print "<table>";
	print "<tr><th colspan=\"10\"># of opponents</th></tr>";
	print "<tr><th></th>";
	for($i=1;$i<=9;$i++) print "<th>$i</th>";
	foreach($file as $line) {
		print "<tr>";
		$fields = explode("\t", trim($line));
		print "<th style=\"text-align: left\">" . $fields[0] . "</th>";
		for($i=1;$i<=9;$i++) {
			$val = $fields[$i] - $sums[$i];
			if($val >= 0) {
				$val += $green_offset_val;
				$cnum = get_cnum($val, $green_offset_val + $max[$i] - $sums[$i]);
				$color = "#{$cnum}ff{$cnum}";
			} else {
				$val = abs($val);
				$val += $red_offset_val;
				$cnum = get_cnum($val, $red_offset_val + $sums[$i] - $min[$i]);
				$color = "#ff{$cnum}{$cnum}";
			}
			print "<td bgcolor=\"$color\">";
			print $fields[$i];
			print "</td>";
		}
		print "</tr>";
	}

	function get_cnum($val, $max) {
		if($val < 0 || $val > $max + .0000001) die("val is $val, max is $max");
		$c = 255 - (($val * 255) / $max);
		$c = dechex($c);
		if(strlen($c) == 1) $c = "0" . $c;
		return $c;
	}
?>
</body>
