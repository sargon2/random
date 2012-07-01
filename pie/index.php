<?

//	function DrawPie($data, $xsize = null, $highlighted = null, $height = null, $viewangle = null, $aliasaccuracy = null) {

	require_once("pie.php");

	$data1=array(10,20,30);
	$data2=array(1,3,9,20);
	$data3 = array();
	for($i=0;$i<10;$i++) $data3[] = mt_rand();
	if($img==1) {
		drawpie($data1,30,null,3,null,10);
		exit();
	}
	if($img==2) {
		drawpie($data2,210,null,6,null,3);
		exit();
	}
	if($img==3) {
		drawpie($data3);
	}
?>

pie 1:<br>
<img src="?img=1"><br>
pie 2:<br>
<img src="?img=2"><br>
Random pie:<br>
<img src="?img=3"><br>
