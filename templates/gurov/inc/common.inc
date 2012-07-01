<?
require_once('inc/db.inc');
if (strstr($GLOBALS['SCRIPT_URL'], '/admin')) {
	require_once('inc/auth.inc');
	session_register('RC');
	$a = mysql_query("select * from permissions where authid='$DEFS[userid]'");
	$i=0;
	while ($b = @mysql_fetch_array($a, MYSQL_ASSOC)) $PERM[] = $b;
	if ($PERM) foreach($PERM as $key=>$value)$PERMlist[] = $value[pname];
} elseif (strstr($GLOBALS['SCRIPT_URL'], '/member')) {
		require_once('inc/auth-member.inc');
		session_register('MM');
}


?>
