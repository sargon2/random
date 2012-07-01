<?
	if(!isset($yearly)) {
		print "<form>amount/year desired: <input type=\"text\" name=\"yearly\"><input type=\"submit\" value=\"submit\"></form>";
		die();
	}
	
	print "to make $yearly per year off of interest...<br>\n";

	print "<table border=1>";
	print "<tr><th>rate</th><th>principle needed</th></tr>";
	for($i=.25;$i<=20;$i+=.25) {
		print "<tr><td>";
		print $i;
		print "%</td><td>\$";
		print number_format($yearly / (exp($i/100)-1));
		print "</td></tr>";
	
	}
	print "</table>";
?>
