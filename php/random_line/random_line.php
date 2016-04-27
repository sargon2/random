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
?>
