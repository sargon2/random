<?
header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
header("Expires: Mon, 26 Jul 1997 05:00:00 GMT"); // Date in the past
?>
This is a collection of links to people who have actual numbers, preferably reproducible, concerning the performance of Java.<br>
<hr>
<br>
People who think native C/C++ is faster than Java:<hr>
<?mklink("http://shootout.alioth.debian.org/u32/benchmark.php?test=all&lang=all");?> (<b>very</b> convincing)<br>
<?mklink("http://www.freewebs.com/godaves/javabench_revisited/");?><br>
<? // Disqualified for having old VM http://verify.stanford.edu/uli/java_cpp.html<br> ?>
<br>
<br>
People who think Java is faster than (or as fast as) native C/C++:<hr>
<?mklink("http://www.idiom.com/~zilla/Computer/javaCbenchmark.html");?><br>
<?mklink("http://www.javaworld.com/jw-02-1998/jw-02-jperf.html");?><br>
<?mklink("http://www.shudo.net/jit/perf/");?><br>
<?mklink("http://kano.net/javabench/");?><br>
<?mklink("http://research.sun.com/techrep/2002/abstract-114.html");?><br>
<?mklink("http://osnews.com/story.php?news_id=5602");?><br>
<br>
The Sun J2SE 5.0 performance white paper: <?mklink("http://java.sun.com/performance/reference/whitepapers/5.0_performance.html");?>

<? function mklink($str) {
	$dstr = htmlentities($str);
	print "<a href=\"$str\">$dstr</a>";
} ?>
