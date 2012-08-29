<html>
<html><head>
<style><!--
table {border-collapse: collapse; }
td {border: 1px solid black; }
//-->
</style></head>
<body>
<?
$link = "http://osiris.978.org/~alex/ups.html";
print "Source: <a href=\"$link\">$link</a><br/>\n<br/>\n";

$codes = array(
        "01" => "UPS United States Next Day Air (\"Red\")",
        "02" => "UPS United States Second Day Air (\"Blue\")",
        "03" => "UPS United States Ground",
        "12" => "UPS United States Third Day Select",
        "13" => "UPS United States Next Day Air Saver (\"Red Saver\")",
        "15" => "UPS United States Next Day Air Early A.M.",
        "22" => "UPS United States Ground - Returns Plus - Three Pickup Attempts",
        "32" => "UPS United States Next Day Air Early A.M. - COD",
        "33" => "UPS United States Next Day Air Early A.M. - Saturday Delivery, COD",
        "41" => "UPS United States Next Day Air Early A.M. - Saturday Delivery",
        "42" => "UPS United States Ground - Signature Required",
        "44" => "UPS United States Next Day Air - Saturday Delivery",
        "66" => "UPS United States Worldwide Express",
        "72" => "UPS United States Ground - Collect on Delivery",
        "78" => "UPS United States Ground - Returns Plus - One Pickup Attempt",
        "90" => "UPS United States Ground - Returns - UPS Prints and Mails Label",
        "A0" => "UPS United States Next Day Air Early A.M. - Adult Signature Required",
        "A1" => "UPS United States Next Day Air Early A.M. - Saturday Delivery, Adult Signature Required",
        "A2" => "UPS United States Next Day Air - Adult Signature Required",
        "A8" => "UPS United States Ground - Adult Signature Required",
        "A9" => "UPS United States Next Day Air Early A.M. - Adult Signature Required, COD",
        "AA" => "UPS United States Next Day Air Early A.M. - Saturday Delivery, Adult Signature Required, COD"
);


header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
header("Expires: Sat, 26 Jul 1997 05:00:00 GMT"); // Date in the past

$code = $_REQUEST['code'];
?><form method="GET">Code: <input type="text" name="code" value="<?=$code?>"/><input type="submit" /></form><?
if(isset($code)) {
        print "code is $code<br/>\n";
        $part = substr($code, 8, 2);
        print "Service code is $part<br/>\n";
        print "<br/>\n";
        print "Service is {$codes[$part]}<br/>\n";
}
print "<br/>\n<br/>\n";
print "All codes:<br/>\n";
print "<table><tr><th>Code</th><th>Service</th></tr>";
foreach($codes as $k=>$v) {
        print "<tr><td>$k</td><td>$v</td></tr>\n";
}
?>
</body>
</html>
