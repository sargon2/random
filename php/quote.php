<?
	class random_line {
		private $currLine = null;
		private $numLines = 0;
		function add_line($line) {
			if(mt_rand(0, $this->numLines) < 1) $this->currLine = $line;
			$this->numLines++;
		}
		function get_line() {
			return $this->currLine;
		}
		function get_num_lines() {
			return $this->numLines;
		}
	}

	$chan = "#hatcave";
	if(preg_match("/^(\.\*)+$/", $args)) unset($args);
	$N = null;
	$r = new random_line();
	if($args) {
#		$args = str_replace('"', '', $args);
#		$args = str_replace("'", '', $args);
		$args = stripslashes($args);
//		$args = escapeshellcmd($args);
		$args = escapeshellarg($args);
		$handle = popen("egrep -h -i " . $args . " /home/sargon/log/$chan/*.log | fgrep -v '> !quote' | fgrep -v ' quotes found: '", "r");
		while(!feof($handle)) {
			$line = fgets($handle);
			if(trim($line) == "") continue;
			$r->add_line($line);
		}
		pclose($handle);
		$N = $r->get_num_lines();
	} else {
		$a = opendir("/home/sargon/log/$chan");
		unset($filelist);
		while (false !== ($file = readdir($a))) {
			if(preg_match("/\.log$/", $file)) {
				if(filesize("/home/sargon/log/$chan/$file") > 1) {
					$filelist[] = $file;
				}
			}
		}
		$file = $filelist[intval(mt_rand(0, count($filelist)-2))];
		$file = "/home/sargon/log/$chan/" . $file;

#		shell_exec("cat /home/sargon/log/*.log | fgrep -v '> !quote' | fgrep -v ' quotes found: ' > $nam");
#		shell_exec("cat $file | fgrep -v '> !quote' | fgrep -v ' quotes found: ' > $nam");
		$handle = popen("fgrep -v '> !quote' $file | fgrep -v ' quotes found: '", "r");
		while(!feof($handle)) {
			$line = fgets($handle);
			if(trim($line) == "") continue;
			$r->add_line($line);
		}
		pclose($handle);
#		$N = trim(shell_exec("fgrep -v '> !quote' /home/sargon/log/$chan/*.log | fgrep -v ' quotes found: ' | wc -l"));
		$N = trim(shell_exec("wc -l /home/sargon/log/$chan/*.log | egrep \"total$\" | awk '{print $1}'")); // fastar
	}
		
	if($N >= 1) {
		print "$N quotes found: ";
		print $r->get_line();
	} else {
		print "No matching quote found";
	}
?>

