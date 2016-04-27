<?
	header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
	header("Expires: Sat, 26 Jul 1997 05:00:00 GMT"); // Date in the past

	// todo: make it clear the characters when they're correct

	if(!isset($count)) $count = 50;

	print "<font size=\"-1\">";

	if(mt_rand(0, 1) < 0.5) {
		print_one("Hiragana", "hiragana.txt");
		print "<br /><br />";
		print_one("Katakana", "katakana.txt");
	} else {
		print_one("Katakana", "katakana.txt");
		print "<br /><br />";
		print_one("Hiragana", "hiragana.txt");
	}

	print "<br /><br /><hr />";
	print "view -> character encoding -> auto-detect -> japanese";

	function print_one($title, $filename) {
		global $count;
		print "$title: <br />&nbsp;";
		$file = file($filename);
		shuffle($file);
		for($i=0;$i<$count;$i++) {
			print trim($file[$i]);
		}
		print "<br />";
		$wid = $count * 4;
		print "<input type=\"text\" size=\"$wid\"/>";
	}
?>
