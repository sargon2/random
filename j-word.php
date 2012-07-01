<?
	header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");
	header("Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT");
	header("Cache-Control: no-store, no-cache, must-revalidate");
	header("Cache-Control: post-check=0, pre-check=0", false);
	header("Pragma: no-cache");

	if(isset($lookup)) {

		$r = get_roman($n, $file);
		header("Location: http://linear.mv.com/cgi-bin/j-e/sjis/tty/dosearch?sDict=on&H=PW&L=J&T=$r&WC=none");
		die();
	}

	$file = file("hiragana.txt");
	foreach($file as $line) { print $line; }
	uprint("<br><br><br>");
	uprint("This page allows you to look up Japanese words with no help from your English or Roman skills.  Click on letters, then on \"lookup\".");
	uprint("<br><br>");
	uprint("<a href=\"?n=\">clear word</a><br><br>");
	uprint("<b>word: ");
	print($n);
	uprint("</b><br><a href=\"?n=");
	print(substr($n, 0, -3));
	uprint("\">backspace</a> ");
	uprint("<br><br>");
	uprint("<table cellpadding=\"3\">");
	$first = true;
	foreach($file as $line) {
		uprint("<tr>");
		$line = str_split($line, 3);
		if($first) array_shift($line);
		$first = false;
		$line = array_map("mklink", $line);
		uprint("<td><font size=\"+1\">");
		$line = implode(utf8_encode("</font></td><td><font size=\"+1\">"), $line);
		print($line);
		uprint("</font></td>");
		uprint("</tr>");
	}
	uprint("</table><br>");
	uprint("<a href=\"?lookup=1&n=");
	print $n;
	uprint("\">lookup</a>");

	function uprint($string) {
		print utf8_encode($string);
	}

	function mklink($content) {
		global $n;
		return "<a href=\"?n=$n$content\">$content</a>";
	}

	function get_roman($word) {
		$h = file("hiragana.txt");
		$file = file("hiragana-r.txt");
		$items = array();
		$first = true;
		foreach($h as $line) {
			$line = rtrim($line, "\r\n");
			$line = str_split($line, 3);
			if($first) array_shift($line);
			$first = false;
			foreach($line as $char) {
				$items[] = $char;
			}
		}
		$items2 = array();
		foreach($file as $line) {
			$line = rtrim($line, "\r\n");
			$line = preg_split("/\s+/", $line);
			foreach($line as $char) {
				$items2[] = $char;
			}
		}
		if(count($items) != count($items2)) {
			print "<pre>";
			print_r($items);
			print_r($items2);
			die("Count doesn't match");
		}
		$lookup = array_combine($items, $items2);
		$letters = str_split($word, 3);
		$outstr = "";
		foreach($letters as $letter) {
			$r = $lookup[$letter];
			$outstr .= $r;
		}
		return $outstr;
	}

?>
