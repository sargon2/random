<pre><?
	$file = file("poker.txt");
	usort($file, "mycomp");

	function mycomp($a, $b) {
		$order = array("s", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A", " ", "\t");
		$order = array_flip($order);
		if($order[$a{2}] < $order[$b{2}]) return 1;
		else if($order[$a{2}] > $order[$b{2}]) return -1;
		if($order[$a{0}] < $order[$b{0}]) return 1;
		else if($order[$a{0}] > $order[$b{0}]) return -1;
		if($order[$a{1}] < $order[$b{1}]) return 1;
		else if($order[$a{1}] > $order[$b{1}]) return -1;
		die("got here");
	}
	foreach($file as  $line) print $line;
?>
