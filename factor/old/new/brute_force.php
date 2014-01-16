<?
	$num = 1313;
	$num = 2062087;
	$num= 62615533;

	for($i=3;$i<=sqrt($num);$i+=2) {
		if($num % $i == 0) die("$i * " . $num/$i . " = $num\n");
	}
?>
