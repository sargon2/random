<?
	require_once("inc/beg.inc");
	$namespace['asdf'] = 'jkl';
	$namespace['varname'] = '$asdf';
	$namespace['numbers'] = array();
	for($i=10;$i>0;$i--) {
		$namespace['*NUMBERS*'][]['value'] = $i;
	}

	for($i=0;$i<10;$i++) {
		for($j=0;$j<10;$j++) {
			$namespace['*NUMBERS2*'][$i]['value'][$j]['value'] = "$i * $j";
		}
	}
	require_once("inc/fin.inc");
?>
