<?
	require_once("match.php");

	test("crickets tickets", "crickets' tickets");
	test("af / b", "af & b");
	test("af and b", "af & b");
	test("interrogate", "interrogate");
	test("interogate", "interrogate");
	test("interrigate", "interrogate");
	test("asdf", "jkl", false);
	test("asdf", "asdr", false);
	test("asdf", "asgr", false);
	test("asdfg", "asdfj");
	test("West Point", "west point");
	test("henry ii", "henry iv", false);
	test("jklasdf", "j k l a s d f");
	test("peanut", "peanuts");
	test("rhodan", "rodan");
	test("clermont", "clairmont", false);
	test("clarmont", "clairmont");
	test("central stuffins", "general stuffins", false);
	test("the Central Powers", "general powers", false);
	test("5 and 10", "the 5 and the 10");
	// kaiser wilhelm, wilhelm
	// pythagoras, pythagorous

	function test($str1, $str2, $should_match = true) {
		testone($str1, $str2, $should_match);
		testone($str2, $str1, $should_match);
	}

	function testone($str1, $str2, $should_match = true) {
		$g = guess_is_right($str1, $str2);
		if($g != $should_match) print "Wrong match: '$str1' '$str2'\n";
	}

?>
