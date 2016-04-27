<?
	$DEFS = array();

	require_once('inc/mysql_func.inc');
	require_once('inc/moo.HTMLT.php');
	require_once('inc/common.inc');
	require_once('inc/functions.inc');
	
	if (!strstr($SCRIPT_NAME, 'CORE')) {
		$MustGeneratePage = 1;
		preg_match('/\/([^\.\/]+)\.php$/', $SCRIPT_NAME , $matches);
		$htmlt = new HTMLT("templates/$matches[1].htmlt");
		$namespace=array_merge($RC, $HTTP_GET_VARS);
	}

?>
