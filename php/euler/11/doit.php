<?
	$file = file("data.txt");
	$data = array();
	$max = 0;
	foreach($file as $line) {
		$row = explode(" ", $line);
		$data[] = $row;
	}
	for($x=0;$x<20;$x++) {
		for($y=0;$y<20;$y++) {
			// horizontal
			check($data[$x][$y], 
				$data[$x+1][$y],
				$data[$x+2][$y],
				$data[$x+3][$y]);
			// vertical
			check($data[$x][$y], 
				$data[$x][$y+1],
				$data[$x][$y+2],
				$data[$x][$y+3]);
			// diagonal
			check($data[$x][$y], 
				$data[$x+1][$y+1],
				$data[$x+2][$y+2],
				$data[$x+3][$y+3]);
			// diagonal 2
			check($data[$x][$y], 
				$data[$x+1][$y-1],
				$data[$x+2][$y-2],
				$data[$x+3][$y-3]);
		}
	}
	function check($a, $b, $c, $d) {
		global $max;
		$p = $a * $b * $c * $d;
		if($p > $max) $max = $p;
	}
	print $max;
?>
