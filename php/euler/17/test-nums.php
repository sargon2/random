<?
	require_once("nums.php");
	check(0, "zero");
	check(1, "one");
	check(10, "ten");
	check(11, "eleven");
	check(20, "twenty");
	check(40, "forty");
	check(21, "twenty one");
	check(55, "fifty five");
	check(99, "ninety nine");
	check(100, "one hundred");
	check(101, "one hundred and one");
	check(410, "four hundred and ten");
	check(414, "four hundred and fourteen");
	check(800, "eight hundred");
	check(999, "nine hundred and ninety nine");
	check(1000, "one thousand");

	function check($num, $expected) {
		$t = get_num($num);
		if($t !== $expected) {
			print "$num failed!! expected $expected but got $t\n";
		}
	}
?>
