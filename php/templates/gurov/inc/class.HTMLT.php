<?
class HTMLT {

	var $filename;
	var $final;
	var $FL;
	var $full;
	var $reg;
	var $method;
	var $parsetimes;
	var $start;
	var $tmpprevns;

	function HTMLT ($filename) {
		$this->filename = $filename;
		$this->reg = 0;
		$this->parsetimes = 0;
		$this->method=1;
		$this->final = '';
		$this->start = gettimeofday();
	}

	function showtime () {
		$end = gettimeofday();
		$start = $this->start[sec] + ($this->start[usec]/1000000);
		$endt = $end[sec]+($end[usec]/1000000);
		return $endt-$start;

	}

	function makepage ($namespace) {
		$this->tmpprevns = $namespace;
		if (is_readable($this->filename)) {
		$this->full = file ($this->filename);
		$this->full = join ('', $this->full);
		} else 
		$this->full = $this->filename;

		$this->parse($this->full, $namespace, 1);
	}

	function SUPA_PARSE($chunk, $namespace, $nskey='') {
		$namespace['u'] = '_';
		$namespace['NSKEY'] = $nskey;
		$array = explode('_', $chunk); $len = count($array);
		for ($i=1;$i<$len;$i=$i+2) {
			if ($array[$i]=='PRINTR') {
				ob_start();
				print_r($namespace);
				$ttt = ob_get_contents();
				ob_end_clean();
				$array[$i] = $ttt;
			} else 
	         $array[$i] = $namespace[$array[$i]];
		}
		return implode('', $array);
	}

	function parse ($chunk, $namespace, $repeat, $nskey = '') {
		if (preg_match('/<!--##([^ ]+) (expr|namespace|file|php|virtual)=([\"\{]([^\"\}])+[\"\}]) [^-]*-->/', $chunk, $matches)) {
			$act = $matches[1];
			$args = substr($matches[3], 1, -1);
			
			
			switch($act) {
################################################################################################################
				case "if":
					$tmp = explode($matches[0], $chunk);
					
					$this->parse($tmp[0], $namespace, 0);
					$n = $namespace;
					$p = $this->tmpprevns;
					if (eval("return ($args);")) $this->parse($tmp[1], $namespace, 0);
					$this->parse($tmp[2], $namespace, 0);
				break;
################################################################################################################
				case "repeat":
					$tmp = explode($matches[0], $chunk);
					$this->parse($tmp[0], $namespace, 0);

					$this->tmpprevns = $namespace;
					if ($namespace[$args]) {
						foreach($namespace[$args] as $key => $value) { $this->parse($tmp[1], $value, 1, $key); }
					}
					$this->parse($tmp[2], $namespace, 0);
				break;
################################################################################################################
				case "include":
					$tmp = explode($matches[0], $chunk);

					$this->parse($tmp[0], $namespace, 0);
					if (strstr($args, '$'))	$args = $namespace[(str_replace('$', '', $args))];
					if ($matches[2]=='file') {
								$fd = file($args);
								$contents = implode("\n", $fd);
					} elseif ($matches[2]=='php') {							
								ob_start();
								require($args);
								$contents = ob_get_contents();
								ob_end_clean();
					} elseif ($matches[2]=='virtual') {
								ob_start();
								virtual($args);
								$contents = ob_get_contents();
								ob_end_clean();
					} else {
								print "fix jo0r shizz";
					}

					
					$this->parse($contents, $namespace, 0);
					$this->parse($tmp[1], $namespace, 0);
						
	 			break;
################################################################################################################
				
				default;
						print "aieeeeeeeeee fix j0 shizz";
				break;	
					
			}
		} else {
			echo $this->SUPA_PARSE($chunk, $namespace, $nskey);
			flush();

		}
	}

}
?>
