<?
	header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
	header("Expires: Mon, 26 Jul 1997 05:00:00 GMT"); // Date in the past
?>
<html>
<head>
<title>Cheap UMPCs</title>
</head>
<body>
<br />
See <a href="http://www.liliputing.com/2008/04/over-past-six-months-or-so-asus-everex_24.html">here</a><br /><br />
List of cheap UMPCs (standard form factor):<br /><hr />
<?
	$umpcs = array(
		array("Eee PC", "http://eeepc.asus.com/global/product.htm"),
		array("Kohjinsha models", "http://www.kohjinsha.com.sg/products.htm"),
		array("HP 2133", "http://h10010.www1.hp.com/wwpc/us/en/sm/WF06b/321957-321957-64295-321838-306995-3687084-3687085-3704509.html"),
		array("Intel Nettop", "http://gizmodo.com/371061/intel-nettop-pictured-in-higher-res-still-looks-promising"),
		array("ECS G10IL", "http://www.ecs.com.tw/ECSWebSite/NewsRoom/NewsDetail.aspx?NewsID=1133&MenuID=13&LanID=0"),
		array("Norhtec Gecko", "http://www.norhtec.com/products/gecko/index.html"),
		array("MSI Wind", "http://gizmodo.com/search/msi%20wind"),
		array("Everex Cloudbook", "http://www.everex.com/products/cloudbook/cloudbook.htm"),
		array("Everex Cloudbook MAX", "http://www.everex.com/products/cloudbook_max/cloudbook_max.htm"),
		array("Pioneer DreamBook Light IL1", "http://www.pioneercomputers.com.au/products/info.asp?c1=3&c2=12&id=2458"),
		// the nanobook is a reference design, not a product
//		array("VIA Nanobook", "http://www.via.com.tw/en/initiatives/spearhead/nanobook/"),
		array("Packard Bell Easynote XS", "http://www.packardbell.co.uk/products/notebooks/easynote-xs/EasyNote-XS20-006/productsheet-PC02F00501-1256.html"),
		array("VyePC models", "http://www.vyepc.com/gallery1.htm"),
		array("Data Evolution Cathena CX", "http://www.dataevolution.com/cathena_cx_info.htm"),
		array("Dell model?", "http://www.engadget.com/2008/04/09/compal-8-9-inch-dell-laptop-coming-in-june-for-less-than-499/"),
		array("Acer model?", "http://www.engadget.com/2008/04/07/more-details-on-acers-eee-pc-competing-laptops-trickle-out/"),
		array("Medion Akoya Mini", "http://www.engadget.com/2008/04/23/medions-akoya-mini-takes-aim-at-the-eee/"),
		array("3k Longitude 400", "http://www.engadget.com/2008/04/22/3k-longitude-400-mini-notebook-youll-never-guess-what-this-r/"),
		array("CTL IL1"),
		array("Dell mini-inspiron", "http://gizmodo.com/393815/exclusive-dell-mini-inspiron-their-first-mini-laptop")
	);

	foreach($umpcs as $a) {
		if(isset($a[1])) {
			print "<a href=\"{$a[1]}\">{$a[0]}</a>";
		} else {
			print $a[0];
		}
		print "<br />";
	}
?>
<hr />
See also <a href="http://www.umpcportal.com/products/">here</a> for ones that didn't make my cut.<br />
Last modified <? print_r(date("r", filemtime(__FILE__))); ?><br />
</body>
</html>
