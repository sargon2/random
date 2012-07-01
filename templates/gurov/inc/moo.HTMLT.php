<?
// //////////////////////////////////////////////////////////////
//
//		The gurov PHP template version 3
//
//   Changes include a nasty bugfix that prevented nested repeats and ifs 
// from working properly
//
//   This library is free software; you can redistribute it and/or
//   modify it under the terms of the GNU Lesser General Public
//   License as published by the Free Software Foundation; either
//   version 2.1 of the License, or (at your option) any later version.
//
//   This library is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
//   Lesser General Public License for more details.
//
//   You should have received a copy of the GNU Lesser General Public
//   License along with this library; if not, write to the Free Software
//   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//
//   Copyright (c) 2000/2001 Gennady Gurov(gurov@bigevilcorp.com)
// //////////////////////////////////////////////////////////////




class HTMLT {

	var $filename;
	var $final;
	var $FL;
	var $full;
	var $reg;
	var $method;
	var $parsetimes;
	var $start;

	function HTMLT ($filename) {
		$this->filename = $filename;
		$this->reg = 0;
		$this->parsetimes = 0;
		$this->method=1;
		$this->final = '';
		$this->start = gettimeofday();
	}

	function makepage ($namespace) {
		if (is_readable($this->filename)) {
		$this->full = file ($this->filename);
		$this->full = join ('', $this->full);
		} else 
		$this->full = $this->filename;

		$this->parse($this->full, $namespace, 1);
#		print $this->final;
	}

################################ all the debug code that was used to find the optimal config for the code
#	function set_method ($method) {	$this->method = $method; }
#	function reset_timer () { $this->start = gettimeofday(); }
#	function debug () {
#		echo 'number of times SUPA_PARSE ran: ';
#		echo $this->reg;
#		echo '<br>';
#		echo 'parse function ran :';
#		echo $this->parsetimes;
#		echo '<br>';
#		print 'from init to debug() time in usec:';
#		$end = gettimeofday();
#		echo $end['usec'] - $this->start['usec'];
#		echo '<br>';
#	}
#
#	function out () { return $this->final; 	}
#######################################################################################
	function SUPA_PARSE($chunk, $namespace) {
		$namespace['u'] = '_';
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

	function parse ($chunk, $namespace, $repeat) {
		if (preg_match('/<!--##([^ ]+) (expr|namespace)=([\"\{]([^\"\}])+[\"\}]) -->/', $chunk, $matches)) {
			$act = $matches[1];
			$args = substr($matches[3], 1, -1);
			
			
			switch($act) {
				case "if":
					$tmp = explode($matches[0], $chunk);
					$this->parse($tmp[0], $namespace, 0);

					$n = $namespace;
		
					if (eval("return ($args);")) $this->parse($tmp[1], $namespace, 0);
					$this->parse($tmp[2], $namespace, 0);
				break;
				
				case "repeat":
					$tmp = explode($matches[0], $chunk);
					$this->parse($tmp[0], $namespace, 0);

					
					if ($namespace[$args]) {
						foreach($namespace[$args] as $key => $value) { $this->parse($tmp[1], $value, 1); }
					}
					$this->parse($tmp[2], $namespace, 0);
				break;
				
				default;
						print "aieeeeeeeeee fix j0 shizz";
				break;	
					
			}
		} else {
#			$this->final .= $this->SUPA_PARSE($chunk, $namespace);
			echo $this->SUPA_PARSE($chunk, $namespace);
			flush();

		}
	}

}
?>
