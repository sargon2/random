6/7/2008 computer builds:<br />
<br />
<table>
<tr><td><?=mklink("sli ddr2-1066", 5073649)?></td><td>$1644.91</td></tr>
<tr><td><?=mklink("non-sli ddr3-1600", 9644168)?></td><td>$1722.92</td></tr>
<tr><td><?=mklink("crossfire ddr3-1600", 5073689)?></td><td>$1802.91</td></tr>
<tr><td><?=mklink("sli ddr3-1333", 9723368)?></td><td>$1976.91</td></tr>
</table>
<?
	function mklink($name, $id) {
		$ret = "<a href=\"http://secure.newegg.com/WishList/PublicWishDetail.aspx?WishListNumber=$id\">$name</a>";
		return $ret;
	}
?>
