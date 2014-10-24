<?
	require_once("inc/quotes.inc");
	$result = mysql_query("select id,rating,quote from rash_quotes order by rand() limit 1;");
	$res = mysql_fetch_assoc($result);
	$id = $res['id'];
	$rating = $res['rating'];
	$quote = html_entity_decode($res['quote']);
	$quote = join(" || ", explode("\n", $quote));
	print "#$id [$rating] $quote";
?>
