<?
	function random() {
		if(mt_rand(0, 1) < 0.5) return true;
		return false;
	}
function dostuff($decks) {
	$suits = array("clubs", "hearts", "diamonds", "spades");
	$cards = array(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13);

	$deck = array();
	for($i=0;$i<$decks;$i++) {
		foreach($suits as $s) {
			foreach($cards as $c) {
				$deck[] = "$c of $s";
			}
		}
	}


	usort($deck, "random");

	$i = 1;
	$count = 0;
	$max = 0;
	$rem = 0;
	foreach($deck as $card) {
		$v = (int)$card;
		switch($v) {
			case 1: $count--; break;
			case 2:
			case 3:
			case 4:
			case 5:
			case 6: $count++; break;
			case 7:
			case 8:
			case 9: break;
			case 10:
			case 11:
			case 12:
			case 13: $count--; break;
		}
		if($count > $max) {
			$max = $count;
			$rem = $i;
		}
//		print "$card ($count)<br>";
		$i++;
	}

	if($rem != 0) $mr = $max/$rem; else $mr = "infinity";
	print "max: $max; rem is $rem, max/rem is $mr<br>";
}
for($i=0;$i<100;$i++) dostuff(6);
?>
