<?
	t_register_block("if", "endif");
	function t_block_if($beginargs, $block) {
		if (eval("return " . $beginargs)) {
			t_parse($block);
		}
	}

	t_register_block("repeat", "endrepeat");
	function t_block_repeat($beginargs, $block) {
		global $namespace;
		if(!isset($namespace[$beginargs])) die("repeat: Cannot find variable $beginargs");
		$nssave = $namespace;
		foreach($nssave[$beginargs] as $var) {
			$namespace[$beginargs] = $var;
			t_parse($block);
		}
		$namespace = $nssave;
	}

	t_register_func("asort");
	function t_func_asort($args) {
		global $namespace;
		asort($namespace[$args]);
	}
?>
