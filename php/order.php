<?
	header("Content-type: text/html; charset=euc-jp");
	$kanji = "�� �� �� �� �� �� Ȭ �� �� �� �� �� �� �� �� ͼ �� �� �� �� �� �� �� ŷ �� ϻ 
 �� �� ʸ �� �� �� �� �� �� �� �� �� �� �� �� �� �� �� �� �� �� �� Ω ɴ ǯ �� 
 �� ̾ �� �� �� �� �� �� �� ¼ �� Į �� �� �� �� ­ �� �� �� �� �� �� �� �� �� 
 �� ��";
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
