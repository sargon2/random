<?
	for($j=0;$j<100;$j++) {

		for($i=0;$i<26;$i++) {
			echo get_letter();
		}
		echo "<br>\n";
	}
	function get_letter() {
		$str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
		return $str{mt_rand(0, strlen($str)-1)};
	}
?>
