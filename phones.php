<?
	$t = array(array("", "droid", "iphone", "my phone (htc mogul)"),
		array("logmein", r("no"), "$30", g("yes (free)")),
		array("screen", g("nice!"), g("pretty nice"), r("shitty")),
		array("physical keyboard", g("yes"), r("no"), g("yes")),
		array("ssh", g("yes"), g("yes"), g("yes")),
		array("removeable battery", g("yes"), r("no"), g("yes")),
		array("price per month", r("$80"), r("$80"), g("$45")),
		array("multitasking", g("yes"), r("no"), g("yes")),
		array("flash (in browser)", r("no"), r("no"), g("yes")),
		array("simultaneous voice+data", r("no"), g("yes"), r("no")),
		array("apps", "10k", g("100k"), "???"),
		array("multitouch", r("no"), g("yes"), r("no"))
	);
	function r($a) {
		return("<font color=\"red\">$a</font>");
	}

	function g($a) {
		return("<font color=\"green\">$a</font>");
	}
	print "11/17/09<br />";
	print "<table>";
	foreach($t as $line) {
		print "<tr>";
		foreach($line as $cell) {
			print "<td>$cell</td>";
		}
		print "</tr>\n";
	}
	print "</table>";
?>
