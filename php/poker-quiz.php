<br /><br /><br /><br /><br /><br /><br /><br /><br /><br />
<center><?
	if(!isset($numplayers)) $numplayers = 5;
	if($numplayers < 2) die("Invalid numplayers $numplayers");

	print "\$numplayers: $numplayers<br>\n";

	$file = file("poker.txt");
	shuffle($file);
	$fields = explode("\t", trim($file[0]));
	$hand = $fields[0];
	$winpercent = $fields[$numplayers-1];
	print "hand: $hand<br>\n";
?><br /><br /><div style="color: white"><?

	$ex = 100 / $numplayers;
	if($winpercent >= $ex) print "stay in<br>\n";
	else if($winpercent == $ex) print "???";
	else print "fold<br>\n";
	print "win percent: $winpercent, expected $ex<br>\n";
	print "</div>";
?>
<br /><br />
select text above here to see answer
<br /><br /><br /><br /><br /><br /><br /><br />
