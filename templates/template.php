<?
//	function t_func_funcname($args) <-- one-liner, such as _ksort var_
//	function t_block_funcname($beginargs, $block) <-- block, such as _repeat var_ and _endrepeat_

	$t_funcs = array();

	require_once("t_funcs.php");

	function t_parse($text) {
		global $t_funcs;
		global $namespace;

		while(strlen($text)) {
			// Advance until we find a $ or an _
			$pos = strpos($text, "$");
			$pos2 = strpos($text, "_");

			$at_var = false;
			$at_func = false;
			if($pos == 0 && $pos2 != 0) {
				$at_func = true;
			}
			else if($pos != 0 && $pos2 == 0) {
				$at_var = true;
			}
			else if($pos != 0 && $pos2 != 0) {
				if($pos < $pos2) $at_var = true;
				else $at_func = true;
			} else {
				print $text;
				$text = '';
				continue;
			}

			// If it's a $, parse the variable
			if($at_var) {
				print substr($text, 0, $pos);
				$text = substr($text, $pos);
				if(substr($text, 0, 2) == "$$") {
					print '$';
					$text = substr($text, 2);
					continue;
				}
				$varname = "";
				if(preg_match('/^\$([a-z][a-z0-9_]*)/i', $text, $matches)) {
					$varname = $matches[1];
					$text = substr($text, strlen($varname)+1);
				} else {
					die("Parse error: '$text'");
				}
				if(isset($namespace[$varname])) {
					print $namespace[$varname];
				} else {
					die("Cannot find variable '\$$varname'");
				}
			}
			if($at_func) { // If it's an _
				$pos = $pos2;
				print substr($text, 0, $pos);
				$text = substr($text, $pos);
				if(substr($text, 0, 2) == "__") {
					print '_';
					$text = substr($text, 2);
					continue;
				}
				$funcname = "";
				if(preg_match('/^\_([a-z][a-z0-9]*)/i', $text, $matches)) {
					$funcname = $matches[1];
					$text = substr($text, strlen($funcname)+1);
				}
				if(isset($t_funcs[$funcname])) {
					// If it's a block function
					if($t_funcs[$funcname] != $funcname) {
						// Parse off begin args
						$pos = strpos($text, '_');
						if(!$pos) die("Misparsed $text");
						$args = substr($text, 1, $pos-1);
						if(strchr($args, '\n')) die("Misparsed $text");
						$text = substr($text, $pos+1);
//						if($text{0} == "\n") $text = ' ' . substr($text, 1);

						// Find end of block
						$pos = find_block_end($funcname, $text);
						if(!$pos) die("Cannot find end of block $funcname");
						$block = substr($text, 0, $pos);
						$text = substr($text, $pos + strlen($t_funcs[$funcname]) + 2);
//						if($text{0} == "\n") $text = substr($text, 1);

						// Call handler function
						$funcname = "t_block_" . $funcname;
						$funcname($args, $block);
					} else { // If it's a normal function
						// Parse off args
						$pos = strpos($text, '_');
						if(!$pos) die("Misparsed $text");
						$args = substr($text, 1, $pos-1);
						if(strchr($args, '\n')) die("Misparsed $text");
						$text = substr($text, $pos+1);

						// Call handler function
						$funcname = "t_func_" . $funcname;
						$funcname($args);
					}
				} else {
					die("'$text' Function name not found: $funcname");
				}
			}
		}
	}

	function find_block_end($funcname, $text) {
		global $t_funcs;
		$ret = 0;
		$level = 0;
		$text = str_replace("__", "", $text);
		$start = true;
		while(1) { // ...
			$pos1 = strpos($text, "_$funcname");
			$pos2 = strpos($text, "_{$t_funcs[$funcname]}");
			if($pos1 == 0 && $pos2 == 0) {
				die("Cannot find block end: $funcname");
			}
			else if($pos1 == 0 && $pos2 != 0) {
				// Next is an end
				$pos = $pos2;
				$start = false;
			}
			else if($pos1 != 0 && $pos2 == 0) {
				// Next is a start
				$pos = $pos1;
				$start = true;
			} else {
				if($pos1 < $pos2) {
					// Next is a start
					$pos = $pos1;
					$start = true;
				} else {
					// Next is an end
					$pos = $pos2;
					$start = false;
				}
			}
			if($start) $level++; else $level--;
			$ret += $pos;
			if($level == -1) return $ret;
			$text = substr($text, $pos+1); $ret++;
		}
	}

	function my_strrpos($haystack, $needle) { // php's strrpos can only handle 1 character
		$haystack = strrev($haystack);
		$needle = strrev($needle);
		return strlen($haystack) - (strpos($haystack, $needle) + strlen($needle));
	}

	function run($filename) {
		$text = file_get_contents($filename);
		t_parse($text);
	}

	function t_register_func($funcname) {
		global $t_funcs;
		$t_funcs[$funcname] = $funcname;
	}

	function t_register_block($begintag, $endtag) {
		if($begintag == $endtag) {
			die("Begin tag may not be the same as end tag: $begintag\n");
		}
		global $t_funcs;
		$t_funcs[$begintag] = $endtag;
	}
?>
