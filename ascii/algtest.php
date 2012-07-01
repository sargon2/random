<?
	$ph = popen("cat /home/sargon/log/#ro/*.2004.log", "r");
	$good = array();
	$linecount = 0;
	while(!feof($ph)) {
		$line = fgets($ph);
		$linecount++;
		if($linecount % 10000 == 0) print $linecount . "\n";
		if($line{24} != '<') continue;
		if(!preg_match("/^.{24}<[^>]+> (.*)$/", $line, $matches)) continue;
		$said = $matches[1];
		$len = strlen($said);
		$chars = array();
		for($i=0;$i<$len;$i++) {
			$v = $said{$i};
			$chars[$v]++;
		}
		$count = count($chars);
		if($len > 40) $len = 40;
		$ratio = ($len / $count);
		$ratio += (countrep($said) * 60) / $len;

		if($len < 35) $ratio -= (35 - $len) * 2;

		$good[$said] = $ratio;
	}

	arsort($good);
	foreach($good as $k=>$v) {
		if($v >= 4) print "BAN: ";
		printf("%02.3f: %s\n", $v, $k);
	}

	function countrep($str) {
		$totcount = 0;
		$currcount = 0;
		$prevchar = "";
		for($i=0;$i<strlen($str);$i++) {
			$currchar = $str{$i};
			if($currchar == $prevchar) {
				$currcount++;
			} else {
				if($currcount > 2) $totcount += $currcount - 2;
			}
			$prevchar = $currchar;
		}
	}

	function spacecount($str) {
		$count = 0;
		$str = preg_replace("/(?!< )  (?! )/", '', $str);
		$str = preg_replace("/(?!< ) (?! )/", '', $str);
		for($i=0;$i<strlen($str);$i++) {
			if($str{$i} == ' ') $count++;
		}
		return $count;
	}
?>
