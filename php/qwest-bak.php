<?
	header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
	header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
	header("Cache-Control: no-store, no-cache, must-revalidate");
	header("Cache-Control: post-check=0, pre-check=0", false);
	header("Pragma: no-cache");
?>
<html><head>
<style><!--
table {border-collapse: collapse; }
td {border: 1px solid black; width: 120px; text-align: center;}
th {width: 120px;}
//-->
</style></head>
<body bgcolor="white">
My situation with Qwest's billing:<br>
<?
	$bills = array();
	$bills['may 2005']['charged'] = 69.38;
	$bills['may 2005']['overcharged'] = 0;
	$bills['may 2005']['reimbursed'] = 0;

	$bills['apr 2005']['charged'] = 69.36;
	$bills['apr 2005']['overcharged'] = 0;
	$bills['apr 2005']['reimbursed'] = 164.49;

	$bills['mar 2005']['charged'] = 51.76;
	$bills['mar 2005']['overcharged'] = 50.37;
	$bills['mar 2005']['reimbursed'] = 69.22;

	$bills['feb 2005']['charged'] = 69.22;
	$bills['feb 2005']['overcharged'] = 50.37;
	$bills['feb 2005']['reimbursed'] = 50.37;

	$bills['jan 2005']['charged'] = 78.77;
	$bills['jan 2005']['overcharged'] = 50.37;
	$bills['jan 2005']['reimbursed'] = 40.84;

	$bills['dec 2004']['charged'] = 0;
	$bills['dec 2004']['overcharged'] = 49.86;
	$bills['dec 2004']['reimbursed'] = 159.22;

	$bills['nov 2004']['charged'] = 118.38;
	$bills['nov 2004']['overcharged'] = 49.86;
	$bills['nov 2004']['reimbursed'] = 0;

	$bills['oct 2004']['charged'] = 191.95;
	$bills['oct 2004']['overcharged'] = 49.35;
	$bills['oct 2004']['reimbursed'] = 0;

	$bills['sep 2004']['charged'] = 152.23;
	$bills['sep 2004']['overcharged'] = 60.01;
	$bills['sep 2004']['reimbursed'] = 0;

	$bills['aug 2004']['charged'] = 73.25;
	$bills['aug 2004']['overcharged'] = 0;
	$bills['aug 2004']['reimbursed'] = 0;

	print "<table>";
	print "<tr>";
	print "<th>Bill</th>";
	print "<th>Charged</th>";
	print "<th>Overcharged</th>";
	print "<th>Reimbursed</th>";
	print "<th>They owe me</th>";
	print "</tr>";
	$they_owe_me = 0;
	$rev = array_reverse($bills);
	$total_over = 0;
	$total_re = 0;
	foreach($rev as $k=>$v) {
		$they_owe_me -= $v['reimbursed'];
		$they_owe_me += $v['overcharged'];
		$bills[$k]['oweme'] = $they_owe_me;

		$total_over += $v['overcharged'];
		$total_re += $v['reimbursed'];
	}
	foreach($bills as $k=>$v) {
		print "<tr><td>";
		print $k;
		print "</td><td>$";
		print $v['charged'];
		print "</td><td>$";
		print $v['overcharged'];
		print "</td><td>$";
		print $v['reimbursed'];
		print "</td><td>$";
		print $v['oweme'];
		print "</td></tr>";
	}
	print "</table>";

	print "<br>";
	print "<b>Total overcharged: \$$total_over</b><br>";
	print "<b>Total reimbursed: \$$total_re</b><br>";

?>
</body></html>
