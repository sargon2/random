<?
        function _print_r($var) {
                print "<pre>";
                print_r($var);
                print "</pre>";
        }

function array_remove($array, $key) {
        foreach($array as $v => $moo) if ($v!=$key) $tmparray[$v] = $moo;
        return $tmparray;
}




function P_REQUIRE($pName, $pValue = 1) {
        global $PERM;
        $found = 0;
        if ($PERM) foreach($PERM as $key => $value) {
                if ($value[pname] == $pName && $value[value] == $pValue) {
                $found = 1;
                }
        }

        return $found;
}
?>
