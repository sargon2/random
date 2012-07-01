<?
	chdir("source1");

	$link = mysql_connect('localhost', 'trivia', 'ttrriivviiaa');
	if(!$link) die("Could not connect to mysql");
	mysql_select_db("GUANTES", $link);
	$er = mysql_error($link);
	if($er) die($er);

	mysql_query("delete from trivia;"); // scary

//	$file = "010104";
	$file = "010204";

	$dir = ".";
	if ($dh = opendir($dir)) {
		while (($file = readdir($dh)) !== false) {
			if(!is_file($file)) continue;
			if(strstr($file, "ans")) continue;
			preg_match("/^\d+/", $file, $matches);
			$file = $matches[0];
			print "File: '$file', ";
			doit($file);
		}
		closedir($dh);
	}


	function doit($filenum) {
		global $link;
		$questions = file($filenum . ".html");
		$answers = file($filenum . "ans.html");

		// Season and air date?

		print "questions: ";
		$questions = parseit($questions);
		print "done, answers: ";
		$answers = parseit($answers);
		print "done\n";

		foreach($questions as $k=>$v) {
			$questions[$k]['answer'] = $answers[$k]['question'];
		}

		$q2 = array();
		foreach($questions as $v) {
			if(stristr($v['question'], "(vid") != "") continue;
			if($v['question'] == "CLUE NOT REVEALED FOR LACK OF TIME") continue;
			if($v['answer'] == "CLUE NOT REVEALED FOR LACK OF TIME") continue;
			if(strstr($v['answer'], "(")) continue;
			if(strstr($v['answer'], ")")) continue;
			if($v['question']{0} == "(") {
				print "q problem: ";
				print_r($v);
			}
			if($v['answer']{0} == "(") {
				print "a problem: ";
				print_r($v);
			}
			$q2[] = $v;
		}

		foreach($q2 as $v) {
			// question, answer, type=round, points=value, category
			$q = mysql_escape_string($v['question']);
			$a = $v['answer'];
			$a = preg_replace("/\?$/", "", $a);
			$a = str_replace('"', "", $a);
			$a = str_replace('.', "", $a);
			$ab = $a;
			$a = preg_replace("/^(who|what)( +)?(i?s|are|were|was)( +)?/i", "", $a);
			if($ab == $a) die("Error parsing -- question part not removed: $a\n");
//			$a = preg_replace("/^(the|a) +/i", "", $a); // done by the matching function
			$a = mysql_escape_string($a);
			$t = mysql_escape_string($v['round']);
			$p = mysql_escape_string($v['value']);
			$c = mysql_escape_string($v['category']);
			$query = "insert into trivia (question, answer, type, points, category) values ('$q', '$a', '$t', '$p', '$c')";

			mysql_query($query, $link);

			$er = mysql_error($link);
			if($er) die($er);
		}
	}

	function parseit($array) {
		$round = "";
		$counter = 0;
		$type = 1;
		$categories = array();
		$ret = array();
		$final = "";
		$final_cat = "";
		foreach($array as $q) {
			$content = "";
			$s = '<TD WIDTH="250"><DIV ALIGN="center"><FONT SIZE="3">';
			if(strncmp($q, $s, strlen($s)) == 0) $content = $q;
			if($content != "") {
				$counter++;
				if($counter == 7) { $counter = 1; $type++; }
				if($counter == 1 && $type == 7) $categories = array();
				switch($type) {
					case 1: $categories[] = strip_tags($content); break;
					case 2: $round = "Round 1"; $value = 200; break;
					case 3: $value = 400; break;
					case 4: $value = 600; break;
					case 5: $value = 800; break;
					case 6: $value = 1000; break;
					case 7: $categories[] = strip_tags($content); break;
					case 8: $round = "Double Jeopardy"; $value = 400; break;
					case 9: $value = 800; break;
					case 10: $value = 1200; break;
					case 11: $value = 1600; break;
					case 12: $value = 2000; break;
					default: die("Parse error: too many matched lines");
				}

				if($type != 1 && $type != 7) {
					$content = str_replace("<BR>", "", $content);
					$content = str_replace("<P>", "", $content);
					$content = preg_replace("/<\/?I>/", "", $content);
					$content = preg_replace('@<FONT COLOR="\w+">[^<]+</FONT( COLOR)?>@', "", $content);
					$qtext = strip_tags($content);
					$qtext = preg_replace("/\([\d ]+\)/", "", $qtext);
					$qtext = trim($qtext);
					if($round == "") die("Parse error: round not set");
					if($value == "") die("Parse error: value not set");
					if($qtext == "") die("Parse error: qtext not set; counter is $counter, type is $type\n");
					$r['round'] = $round; 
					$r['value'] = $value;
					$r['question'] = $qtext;
					$r['category'] = trim($categories[$counter - 1]);

					$ret[] = $r;
				}
			}

			$s = '<TD><FONTSIZE="3"><DIV ALIGN="center">'; if(strncmp($q, $s, strlen($s)) == 0 && $final == "") $final = trim(strip_tags($q));
			$s = '<TD><FONT SIZE="3"><DIV ALIGN="center">'; if(strncmp($q, $s, strlen($s)) == 0 && $final == "") $final = trim(strip_tags($q));
			$s = '<TD><DIV ALIGN="center"><FONT SIZE="3"><B>'; if(strncmp($q, $s, strlen($s)) == 0 && $final_cat == "") $final_cat = trim(strip_tags($q));
			$s = '<TD><DIV ALIGN="center"><FONT="3"><B>'; if(strncmp($q, $s, strlen($s)) == 0 && $final_cat == "") $final_cat = trim(strip_tags($q));


		}

		if($final === "") die("Parse error: final not set");
		if($final_cat == "") die("Parse error: final_cat not set");
		$r['round'] = "Final Jeopardy";
		$r['value'] = 2500;
		$r['question'] = $final;
		$r['category'] = $final_cat;
		$ret[] = $r;
		return $ret;
	}
?>
