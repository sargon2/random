<pre>
Snopes articles which surprised me:

<?
	$urls = array(
		'http://www.snopes.com/quotes/signature/elementary.asp',
		'http://www.snopes.com/science/coriolis.asp',
		'http://www.snopes.com/food/ingredient/turkey.asp',
		'http://www.snopes.com/autos/law/redcars.asp',
		'http://www.snopes.com/college/homework/unsolvable.asp',
		'http://www.snopes.com/holidays/christmas/immaculate.asp',

		'http://www.snopes.com/college/admin/cent.asp',
		'http://www.snopes.com/autos/grace/sugar.asp',
		'http://www.snopes.com/business/origins/chips.asp',
		'http://www.snopes.com/business/market/atari.asp',
		'http://www.snopes.com/critters/wild/dogyears.htm',
		'http://www.snopes.com/horrors/vanities/tapeworm.asp',
		'http://www.snopes.com/movies/actors/chaplin2.htm',
		'http://www.snopes.com/cokelore/cocaine.asp',
		'http://www.snopes.com/food/ingredient/jello.asp',
		'http://www.snopes.com/science/cricket.asp',
		'http://www.snopes.com/legal/postal/sendcash.asp',
		'http://www.snopes.com/food/ingredient/carrots.asp'
		);
	foreach($urls as $url) {
		print "<a href=\"$url\">$url</a>\n";
	}
?>

Snopes articles that confirmed what I already knew, but that
other people tried to convince me of:

<?
	$urls2 = array(
		'http://www.snopes.com/business/genius/spacepen.asp',
		'http://www.snopes.com/critters/wild/longlegs.htm',
		'http://www.snopes.com/science/stats/10percnt.htm',
		'http://www.snopes.com/science/stats/spiders.htm',
		'http://www.snopes.com/business/consumer/cookie.asp',
		'http://www.snopes.com/business/secret/carmex.asp',
		'http://www.snopes.com/critters/crusader/bonsai.asp'
	);
	foreach($urls2 as $url) {
		print "<a href=\"$url\">$url</a>\n";
	}
?>

Not snopes, but Einstein didn't fail math: <a href="http://www.time.com/time/2007/einstein/3.html">http://www.time.com/time/2007/einstein/3.html</a>
Also, cow tipping is a myth: <a href="http://en.wikipedia.org/wiki/Cow_tipping">http://en.wikipedia.org/wiki/Cow_tipping</a>
