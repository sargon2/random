<?

# error.php
# Makes errors more useful, printing a backtrace with all errors PHP allows us to hook.
	
	$ERROR = false;

	# Since the shutdown process is aborted if a registered shutdown function calls exit,
	# we can abort the deallocation process in the event of an error.
	# This allows us to just return inside ErrorHandler if we want to ignore an error.
	function _exitWithoutShutdown() {
		global $ERROR;
		if($ERROR) {
			exit();
		}
	}

	function print_file_part($file, $line) {
		$line--;
		$file = file($file);

		$start = $line - 3;
		if($start < 0) $start = 0;

		$end = $line + 4;
		if($end > count($file)) $end = count($file);


		print "<pre>";
		for($i=$start;$i<$end;$i++) {
			$l = sprintf("%5d", $i + 1);
			print "$l: ";
			$file[$i] = str_replace("\t", "        ", $file[$i]);
			$file[$i] = htmlentities($file[$i]);
			if($i == $line) $file[$i] = preg_replace("/^(\s*)(.*)$/i", "$1<u>$2</u>", $file[$i]);
			print $file[$i];
		}
		print "</pre>";
	}

	function ErrorHandler($errno, $errstr, $errfile, $errline) {
//		if($errno == 8) return;
//		if($errno == 2) return; // array_merge php5 thing
		global $ERROR;
		$ERROR = true;

		$errstr = htmlentities($errstr);
		$errstr = "<span style=\"font-family: monospace; font-size: 14px\">$errstr</span>";

		# Get the backtrace
		$back = debug_backtrace();
//		print "<pre>"; print_r($back); print "</pre>";

		print "<br /><b>Error</b> (level $errno): <br />\n<br />\n$errstr<br />\n<br />\n";

//		array_shift($back); // first one is always ErrorHandler
		foreach($back as $item) {
			if(isset($item['args'][4])) $item['args'] = $item['args'][4]; // hack since debug_backtrace is broken
			if(!isset($item['args'])) {
				print "in ";
			}
			if(isset($item['class'])) {
				print '<b>' . htmlentities($item['class'] . $item['type']) . '</b>';
			}
			if(isset($item['function'])) {
				print "<b>" . $item['function'] . "</b>";
				if(isset($item['args'])) {
					print "(";
					$stuff = array();
					foreach($item['args'] as $arg) {
						if($arg === null) $arg = "null";
						if(is_array($arg)) $arg = "Array";
						$stuff[] = "<span style=\"font-family: monospace; font-size: 14px\">$arg</span>";
					}
					print implode(", ", $stuff);
					print ") called on ";
				} else {
					print "() on ";
				}
			}
			if(isset($item['line'])) {
				print "line <b>{$item['line']}</b> of file '<b>{$item['file']}</b>':<br />";
				print_file_part($item['file'], $item['line']);
			} else {
				print "<br />";
			}
		}

		exit();
	}
	# There is no reason to ignore any warning or error.
	error_reporting(E_ALL | E_STRICT);

	# set up the true-die function
	register_shutdown_function("_exitWithoutShutdown");

	# Set up the hook.
	set_error_handler("ErrorHandler");
?>
