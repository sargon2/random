<?
	require_once("convert.php");
	assertAll('a', 0);
	assertAll('za', 0);
	assertAll('s', 1);
	assertAll('zs', -1);
	assertAll('d', 2);
	assertAll('zd', -2);
	assertAll('f', 3);
	assertAll('sa', 4);
	assertEq(convertToNum('j'), 0);
	assertEq(convertToNum('zzz'), 0);
	assertEq(convertToNum('%'), 0);
	assertEq(convertToNum(''), 0);
	assertEq('a', convertToLetters(0.5));
	assertEq(0, convertToNum('a.b'));

	function assertAll($letters, $num) {
		assertEq($num, convertToNum($letters), $letters);
		assertEq($letters, convertToLetters($num), $num);
		assertEq($num, convertToNum(convertToLetters($num)), convertToLetters($num));
		assertEq($letters, convertToLetters(convertToNum($letters)), convertToNum($letters));
		assertEq($letters, eitherway($num));
		assertEq($num, eitherway($letters));
	}
	function assertEq($a, $b, $msg = "") {
		if($a === "za") $a = "a";
		if($b === "za") $b = "a";
		if($a !== $b) {
			print "$a !== $b ($msg)\n";
		}
	}
?>
