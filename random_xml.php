<?
	header("Content-Type: text/xml");
	$levels = 0;
	print "<asdf level=\"0\">\n";
	for($i=0;$i<mt_rand(100,200);$i++) {
		$dostuff = mt_rand(0, 1);
		switch($dostuff) {
			case 0:
				for($i=0;$i<=$levels;$i++) print "    ";
				print "<asdf level=\"" . ($levels+1) . "\">asdf\n";
				$levels++;
			break;
			case 1:
				if($levels > 0) {
					for($i=0;$i<$levels;$i++) print "    ";
					print "</asdf>\n";
					$levels--;
				}
			break;
			default:
				die("invalid dostuff");
			break;
		}
	}

	for(;$levels>0;$levels--) {
		for($i=0;$i<$levels;$i++) print "    ";
		print "</asdf>\n";
	}
	print "</asdf>\n";

?>
