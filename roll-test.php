<?
$ret = array();
for($j=0;$j<100000;$j++) {
	$args = "1d10";
  if(!$args)
    die("roll some dice...  usage: roll <number of dice>d<faces>, like 3d6");
  $args = str_replace("d", " ", $args);
  $argv = explode(" ", $args);
  $argv[0] = 0 + $argv[0];
  $argv[1] = 0 + $argv[1];
  $val = 0;
  if($argv[0] > 10000) die("too big");
  if($argv[1] > 10000) die("too big");
  if($argv[0] <= 0) die("too small");
  if($argv[1] <= 0) die("too small");
  for($i=0;$i<$argv[0];$i++) {
    @$val2 = mt_rand(1,$argv[1]);
    if($val2 == 0) die("Error rolling dice");
    if(($argv[0] <= 10) && ($argv[0] != 1)) print $val2 . " ";
    $val += $val2;
  }
  if(($argv[0] <= 10) && ($argv[0] != 1)) print ": ";
	$ret[$val]++;
}
print_r($ret);
?>
