<?
	header("Content-type: text/html; charset=euc-jp");
	$kanji = "°ì ¶å ¼· Æó ¿Í Æþ È¬ ÎÏ ½½ ²¼ »° Àé ¾å ¸ý ÅÚ Í¼ Âç ½÷ »Ò ¾® »³ Àî ¸Þ Å· Ãæ Ï» 
 ±ß ¼ê Ê¸ Æü ·î ÌÚ ¿å ²Ð ¸¤ ²¦ Àµ ½Ð ËÜ ±¦ »Í º¸ ¶Ì À¸ ÅÄ Çò ÌÜ ÀÐ Î© É´ Ç¯ µÙ 
 Àè Ì¾ »ú Áá µ¤ ÃÝ »å ¼ª Ãî Â¼ ÃË Ä® ²Ö ¸« ³­ ÀÖ Â­ ¼Ö ³Ø ÎÓ ¶õ ¶â ±« ÀÄ Áð ²» 
 ¹» ¿¹";
	$kanji = split(" ", $kanji);
	$a = array();

	$num = 1;
	$max = 10000;
	while(count($a) < $max) {
		add($num, find_first_open($a, $num), $max);
		$num++;
	}

	ksort($a);
	foreach($a as $v) {
		print $kanji[$v-1] . " ";
	}

	function find_first_open($a, $num) {
		$i = 1;
		while(isset($a[$i]) || $a[$i-1] == $num) $i++;
		return $i;
	}

	function add($num, $start_pos, $end_pos) {
		$increment = 1;
		$i = $start_pos;
		while($i <= $end_pos) {
			add_incr($num, $i);
			$i += $increment;
			$increment++;
		}
	}

	function add_incr($num, $i) {
		global $a;
		while(isset($a[$i]) || $a[$i-1] == $num) $i++;
		$a[$i] = $num;
	}
?>
