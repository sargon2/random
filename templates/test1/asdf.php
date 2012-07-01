<?
	function parse_vars($filename, $namespace) {
		$placeholder = '722ccea1b57c8';
		$file = file($filename);
		$ret = "";
		foreach($file as $line) {
			$line = str_replace('$$', $placeholder, $line);
			$line = explode('$', $line);
			$first = true;
			foreach($line as $token) {
				if($first) {
					$ret .= $token;
					$first = false;
					continue;
				}
				if(preg_match("/^([a-z][a-z0-9]*)(.*)$/", $token, $matches)) {
					$varname = $matches[1];
					if(isset($namespace[$varname])) {
						$ret .= $namespace[$varname] . $matches[2] . "\n";
					} else {
						$ret .= '$' . $token;
					}
					continue;
				}
				$ret .= '$' . $token;
			}
		}
		$ret = str_replace($placeholder, '$', $ret);
		return $ret;
	}

	$filename = "./test.t";
	$namespace['asdf'] = 'jkl';
	$namespace['varname'] = '$asdf';
	print parse_vars($filename, $namespace);
?>
