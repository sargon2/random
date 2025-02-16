<?
header("Cache-Control: no-cache, must-revalidate"); // HTTP/1.1
header("Expires: Sat, 26 Jul 1997 05:00:00 GMT"); // Date in the past
?>
<!DOCTYPE html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>kanji</title>
<script>
function selectId(id) {
        document.getElementById(id).select();
}
</script>
</head>
<body>
<?
$common_url = "http://jisho.org/words?jap=*%s*&eng=&dict=edict&common=on";
$uncommon_url = "http://jisho.org/words?jap=*%s*&eng=&dict=edict&common=off";

?><form>Kanji:<input type="text" name="kanji" value="<?=$kanji?>"/><input type="submit"/></form><?

if(!isset($kanji)) exit();

print "<pre>";
$count = doit($common_url, 1);
if($count < 10)
        doit($uncommon_url, 2);
print "</pre>";

function doit($url, $id) {
        global $kanji;
        $full_url = sprintf($url, urlencode($kanji));
        $contents = file_get_contents($full_url);
        ?><a href="<?=$full_url?>"><?=$full_url?></a><?

        $dom = new DOMDocument;
        @$dom->loadHTML($contents);
        $content = $dom->getElementById("result_content");
        print "<br /><br />";
        print "<form>";
        print "Kanji: " . $kanji . "<br /><br />";
        $meanings = array();
        $context = "";
        if(!$content) return 0;
        foreach($content->getElementsByTagName("tr") as $tr) {
                $tds = $tr->getElementsByTagName("td");
                $data = array();
                foreach($tds as $item) {
                        $data[] = $item->nodeValue;
                }
                if(isset($data[2])) {
                        $named_data['kanji'] = trim(utf8_decode($data[0]));
                        $named_data['kana'] = trim(utf8_decode($data[1]));
                        $named_data['meanings'] = $data[2];
                        $meanings[$named_data['kanji']] = $named_data['meanings'];
                        $named_data['kanji'] = str_replace($kanji, "＿", $named_data['kanji']);
                        # TODO: show furigana only for the kanji, not for the okurigana
                        $context = $context . $named_data['kanji'] . '[' . $named_data['kana'] . ']   ';
                }
        }

        $context = trim($context);
        print "<button type=\"button\" onclick=\"selectId('context" . $id . "')\">select</button>";
        print "<input type=\"text\" style=\"width: 90%\" id=\"context" . $id . "\" value=\"" . $context . "\"/>";
        print "</form>";

        print "<br /><br /><br />Meanings:<br />";

        foreach($meanings as $k=>$meaning) {
                print "$k: $meaning<br />";
        }
        print "<br /><br /><br />";
        return count($meanings);
}

?>
</body>
