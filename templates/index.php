<?
	require_once("template.php");
	$namespace['asdf'] = 'jkl';
	$namespace['varname'] = '$asdf';
	$namespace['numbers'] = array();
	for($i=10;$i>0;$i--) {
		$namespace['numbers'][] = $i;
	}

	for($i=0;$i<10;$i++) {
		for($j=0;$j<10;$j++) {
			$namespace['numbers2'][$i][$j] = "$i * $j";
		}
	}

	$namespace['user_id'] = 3;
//	run('test.t');
	run('gurovcomp.t');
?>
