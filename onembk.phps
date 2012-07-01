<?php
require '/home/michael/public_html/.inc/head.inc';
$project = getvar('project');
$rep_type = getvar('rep_type');
$smp_element = getvar('smp_element');
$disfile = getvar('disfile');
$lisfile = getvar('lisfile');
$tmpvar = getvar('detailed_numerics');
$saveas = getvar('saveas');
$count_zero = getvar('count_zero');
$doubble_space = getvar('doubble_space');
if (isset($tmpvar)) {
    $_SESSION['detailed_numerics'] = $tmpvar;
    unset($tmpvar);
}
$batches = array();
$dispcodes = array();
$questions = array();
foreach ($_REQUEST as $key => $value) {
    if (stristr($key, 'batch')) {
        $batches[] = $value;
    }
    if (stristr($key, 'disp')) {
        $dispcodes[] = $value;
    }
    if (stristr($key, 'quest')) {
        $questions[] = $value;
    }
}
$batches_selected = false;
if (count($batches) > 0) {
    $batches_selected = true;
}
$disps_selected = false;
if (count($dispcodes) > 0) {
    $disps_selected = true;
}
$questions_selected = false;
if (count($qnums) > 0) {
    $questions_selected = true;
}
if ((trim($rep_type) == '') || (trim($project) == '')) {
?>
<br>
<br>
<br>
<form name="choosereport" action="" method="post">
    Enter a project number:<br>
    <input type="text" name="project"><br><br>

    <input type="hidden" name="rep_type" value="0">
    <!-- What type of report would you like to run?<br>
    <input checked type="radio" name="rep_type" value="0"> Marginal<br>
    <input disabled type="radio" name="rep_type" value="1"> Cross Tab <i> - disabled</i><br>
    <input disabled type="radio" name="rep_type" value="2"> Straight Tab <i> - disabled</i><br><br> -->

    <input type="submit" value="submit">
</form>
<?php
} elseif (!$batches_selected || !$disps_selected) {
    $tmpdir = opendir("/{$proj_path}");
    while ($v = readdir($tmpdir)) {
        if (stristr(basename($v), $project . ".")) {
            $dir[] = $v;
        }
    }
    closedir($tmpdir);
    $batch_list = array();
    for ($i = 0; $i < count($dir); $i++) {
        if (is_file($proj_path . $dir[$i])) {
            if (strtolower($dir[$i]) == strtolower($project) . ".dis") {
                $disfile = $dir[$i];
                global $disfile;
            }
            if (strtolower($dir[$i]) == strtolower($project) . ".lis") {
                $lisfile = $dir[$i];
            }
            $tmpfile = fopen($proj_path . $dir[$i], "r");
            $tmp = fgetc($tmpfile);
            fclose($tmpfile);
            if ($tmp == '5') {
                $batch_list[] = $dir[$i];
            }
        }
    }
    $disps = array();
    $linecount = 0;
    $tmpfile = fopen($proj_path . $disfile, "r");
    while ($tmpline = fgets($tmpfile)) {
        $linecount++;
        if ((trim(substr($tmpline, 0, 5)) !== '') && (trim(substr($tmpline, 0, 5)) !== '<User')) {
            $disps[$linecount] = trim(substr($tmpline, 0, 35));
        }
    }
    $listing = read_listing($proj_path, $lisfile);
    $_SESSION['listing'] = $listing;
?>
<form name="selectoptions" action="" method="post">
    <center><input type="submit" value="submit"><br> - or - <br>
    Select options and filters:</center>
    <table border="1" width="100%">
        <tr>
            <td valign="top">
                <table width="100%">
                    <tr>
                        <td colspan="3">
                            <center>Enter output file name: <input type="text" size="15" value="<?php echo $project . ".MAR"; ?>" name="saveas"> (this will save in 'k:\')</center>
                        </td>
                    </tr>
                    <tr>
                        <td width="45%" valign="top">
                            <br>
                            <?php
                            choose_batches($proj_path, $project, 'selectoptions', 'all', 'batch', 1);
                            ?>
                            <input type="hidden" name="rep_type" value="<?php echo $rep_type; ?>">
                            <input type="hidden" name="project" value="<?php echo $project; ?>">
                            <input type="hidden" name="disfile" value="<?php echo $disfile; ?>">
                            <input type="hidden" name="lisfile" value="<?php echo $lisfile; ?>">
                            <br>
                        </td>
                        <td width="55%" valign="top">
                            <br>
                            <?php
                            choose_questions($proj_path, $project, 'selectoptions', 'quest', 4);
                            ?>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td valign="top">
                <table width="100%">
                    <tr>
                        <td width="45%" valign="top">
                            <br>Numeric options:<br><br>

                            <input checked type="radio" name="detailed_numerics" value="0"> Standard numeric printing<br>
                            <input type="radio" name="detailed_numerics" value="1"> Detailed numeric printing<br>&nbsp;&nbsp;&nbsp;(now displays sub-totals)<br>
                            <input checked type="checkbox" name="count_zero" value="1"> Count "0" as a punch<br><br>

                            Formatting options:<br><br>

                            <input type="checkbox" name="doubble_space" value="1"> Doubble-space frequiencies
                        </td>
                        <td width="55%" valign="top">
                            <br>
                            <?php
                            choose_dispositions($proj_path, $project, 'selectoptions', 'disp', 2);
                            ?>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
    <br>
</form>
<?php
} else {
    $data = array();
    $tmp = batch_info($batches, $proj_path, $dispcodes);
    $data = $tmp['alldata'];
    unset($tmp);
    echo "<br>\r\nGenerating report for $project, please wait<br>\r\n";
    flush();
    $listing = read_listing($proj_path, $lisfile);
    $total_resps = 0;
    foreach ($data as $key => $val) {
        foreach ($val as $key2 => $val2) {
            show_prog(2500);
            if (($data[$key][$key2][0] !== '5') && ($data[$key][$key2][0] !== '7') && ($data[$key][$key2][0] !== '8') && ($data[$key][$key2][0] !== '9')) {
                $cur_q = trim(substr($data[$key][$key2], 4, 3));

                //for coded projects
                if ($data[$key][$key2][0] == '6') {$listing[$cur_q]['qtype'] = 'NOE';}

                if (($cur_resp !== $tmp_resp) || ($cur_q !== $tmp_q)) {
                    $listing[$cur_q]['maxqual'] = $listing[$cur_q]['maxqual'] + 1;
                }
                $tmp_resp = $cur_resp;
                $tmp_q = $cur_q;
                $cur_data = trim(substr($data[$key][$key2], 11, strlen($data[$key][$key2]) - 11));
            } else {
                if ($data[$key][$key2][0] == '5') {
                    $total_resps++;
                    $cur_resp = trim(substr($data[$key][$key2], 2, 6));
                }
                $cur_q = '';
            }
            if (in_array($cur_q, $questions)) {
                if ($listing[$cur_q]['qtype'] == 'CE') {
                    if (!is_array($listing[$cur_q]['atext'][trim(substr($data[$key][$key2], 11, 3))])) {
                        $listing[$cur_q]['atext'][trim(substr($data[$key][$key2], 11, 3))] = array();
                    }
                    $a_key = array_keys($listing[$cur_q]['atext'][trim(substr($data[$key][$key2], 11, 3))]);
                    $listing[$cur_q]['atext'][trim(substr($data[$key][$key2], 11, 3))][$a_key[0]]++;
                } elseif ($listing[$cur_q]['qtype'] == 'NCE') {
                    $a_key = array_keys($listing[$cur_q]['atext'][trim(substr($data[$key][$key2], 9, 2))]);
                    if (!is_array($listing[$cur_q]['atext'][trim(substr($data[$key][$key2], 9, 2))][$a_key[0]])) {
                        $listing[$cur_q]['atext'][trim(substr($data[$key][$key2], 9, 2))][$a_key[0]] = array();
                    }
                    $listing[$cur_q]['atext'][trim(substr($data[$key][$key2], 9, 2))][$a_key[0]][$cur_data]++;
                } elseif ($listing[$cur_q]['qtype'] == 'OE') {
                    if ($skipq !== $cur_q) {
                        $a_key = array_keys($listing[$cur_q]['atext'][1]);
                        $listing[$cur_q]['atext'][1][$a_key[0]]++;
                        $skipq = $cur_q;
                    }
                } elseif ($listing[$cur_q]['qtype'] == 'NOE') {
                    if ($skipq !== $cur_q) {
                        $a_key = array_keys($listing[$cur_q]['atext'][1]);
                        if (!is_array($listing[$cur_q]['atext'][1][$a_key[0]])) {
                            $listing[$cur_q]['atext'][1][$a_key[0]] = array();
                        }
                        $listing[$cur_q]['atext'][1][$a_key[0]][$cur_data]++;
                        $skipq = $cur_q;
                    }
                } elseif ($listing[$cur_q]['qtype'] == 'FORMULA') {
                    if ($skipq !== $cur_q) {
                        $a_key = array_keys($listing[$cur_q]['atext'][1]);
                        if (!is_array($listing[$cur_q]['atext'][1][$a_key[0]])) {
                            $listing[$cur_q]['atext'][1][$a_key[0]] = array();
                        }
                        $listing[$cur_q]['atext'][1][$a_key[0]][$cur_data]++;
                        $skipq = $cur_q;
                    }
                }
            }
        }
    }
    $martext = '';
    echo "<pre>";
    $martext .= "\r\n\r\nProject: $project; Total qualified respondents: $total_resps;\r\n\r\n";
    $newval4 = 0;
    if ($_SESSION['detailed_numerics'] == '0') {
        $detailed_numerics = false;
    } else {
        $detailed_numerics = true;
    }
    if ($doubble_space == '1') {
        $dspace = "\r\n\r\n";
    } else {
        $dspace = "\r\n";
    }
    $firstrun = true;
    foreach ($listing as $key => $val) {
        if (in_array($key, $questions)) {
            if (($tmpkey !== $key) && (!$firstrun)) {
                if (trim($listing[$tmpkey]['maxqual']) == '') {
                    $listing[$tmpkey]['maxqual'] = '0';
                    $tmp_this_perc = fill_string('0%', 4, ' ', 'left');
                } else {
                    $tmp_this_perc = '100%';
                }
                $martext .= "\r\n " . fill_string("Total Qualified:", 72, ' ', 'left') . fill_string(($listing[$tmpkey]['maxqual'] + 0), 4, ' ', 'left') . "   " . fill_string(number_format($tmp_this_perc, 2) . "%", 7, ' ', 'left') . "   " . number_format(bcdiv($listing[$tmpkey]['maxqual'], $total_resps, 3) * 100, 2) . "%\r\n";
                $martext .= "\r\n\r\n" . fill_string('_', 100, '_', 'left') . "\r\n\r\n";
            }
            $tmpkey = $key;
            $firstrun = false;
            $martext .= str_replace("\n", "\r\n", $listing[$key]['qtext']) . "\r\n\r\n " . fill_string(' ', 71, ' ', 'left') . "Count   %ThisQ    %Total \r\n " . fill_string(' ', 71, ' ', 'left') . "-----   -------   -------$dspace";
            foreach ($listing[$key]['atext'] as $key2 => $val2) {
                if ($key2 > 0) {
                    foreach ($val2 as $key3 => $val3) {
                        if (!is_array($val3)) {
                            if (($key3{0} !== '#') || ($val3 > 0)) {
                                if (trim($listing[$key]['maxqual']) !== '') {
                                    $tmp = $val3 / $listing[$key]['maxqual'] * 100;
                                    $tmp = number_format($tmp, 2);
                                    $this_perc = fill_string(substr($tmp, 0, 5) . '%', 6, ' ', 'left');
                                } else {
                                    $this_perc = '0.00%';
                                }
                                $martext .= " " . fill_string(fill_string($key2, 3, ' ', 'right') . " > $key3", 72, ' ', 'left') . fill_string($val3, 5, ' ', 'left') . "  " . fill_string(number_format($this_perc, 2) . "%", 7, ' ', 'left') . "   " . fill_string(number_format(bcdiv($val3, $total_resps, 3) * 100, 2) . "%", 5, ' ', 'left') . $dspace;
                            }
                        } else { //numerics in here
                            uksort($val3, 'nocase');
                            if (($detailed_numerics) && ($listing[$key]['qtype'] == 'NCE')) {
                                $martext .= " " . fill_string($key2, 3, ' ', 'right') . " > " . $key3 . $dspace;
                            }
                            foreach ($val3 as $key4 => $val4) {
                                if (trim($listing[$key]['maxqual']) !== '') {
                                    $tmp = $val4 / $listing[$key]['maxqual'] * 100;
                                    $tmp = number_format($tmp, 2);
                                    $this_perc = fill_string($tmp . '%', 7, ' ', 'left');
                                } else {
                                    $this_perc = fill_string(number_format(0, 2) . '%', 7, ' ', 'left');
                                }
                                if ($detailed_numerics) {
                                    if ($listing[$key]['qtype'] == 'NCE') {
                                        $last_key4 = $key4;
                                        if ($count_zero == '1') {
                                            $martext .= "     " . fill_string("($key4)", 68, ' ', 'left') . fill_string($val4, 5, ' ', 'left') . "  " . $this_perc . "   " . fill_string(number_format(bcdiv($val4, $total_resps, 3) * 100, 2) . "%", 6, ' ', 'left') . $dspace;
                                            $val_tot = $val_tot + $val4;
                                            $print_tot = true;
                                        } else {
                                            if ($key4 > 0) {
                                                $martext .= "     " . fill_string("($key4)", 68, ' ', 'left') . fill_string($val4, 5, ' ', 'left') . "  " . $this_perc . "   " . fill_string(number_format(bcdiv($val4, $total_resps, 3) * 100, 2) . "%", 6, ' ', 'left') . $dspace;
                                                $val_tot = $val_tot + $val4;
                                                $print_tot = true;
                                            }
                                        }
                                    } else { // 'NOE' here
                                        $martext .= "  " . fill_string(fill_string($key2, 3, ' ', 'right') . " > $key3 ($key4)", 71, ' ', 'left') . fill_string($val4, 5, ' ', 'left') . "  " . $this_perc . "   " . fill_string(number_format(bcdiv($val4, $total_resps, 3) * 100, 2) . "%", 6, ' ', 'left') . $dspace;
                                    }
                                    $totalval = $totalval + $val4;
                                } else {
                                    if ($count_zero == '1') {
                                        $newval4 = $newval4 + $val4;
                                    } else {
                                        /* This if() statement will stop the marginal from counting '0' as a punch.
                                           This only matters if $detalied_numerics === false. */
                                        if ($key4 > 0) {
                                            $newval4 = $newval4 + $val4;
                                        }
                                    }
                                }
                            }
                            if (!$detailed_numerics) {
                                $tmp = $newval4 / $listing[$key]['maxqual'] * 100;
                                $tmp = number_format($tmp, 2);
                                $this_perc = fill_string($tmp . '%', 7, ' ', 'left');
                                $martext .= " " . fill_string(fill_string($key2, 3, ' ', 'right') . " > $key3", 62, ' ', 'left') . "          " . fill_string($newval4, 5, ' ', 'left') . "  " . $this_perc . "   " . fill_string(number_format(bcdiv($newval4, $total_resps, 5) * 100, 2) . "%", 6, ' ', 'left') . $dspace;
                                $newval4 = 0;
                            } else {
                                if ($print_tot) {
                                    $martext .= "     " . fill_string("(Total:)", 68, ' ', 'left') . fill_string($val_tot, 5, ' ', 'left') . "  " . fill_string(number_format($val_tot / $listing[$key]['maxqual'] * 100, 2) . '%', 7, ' ', 'left') . "   " . fill_string(number_format(bcdiv($val_tot, $total_resps, 3) * 100, 2) . "%", 6, ' ', 'left') . "\r\n" . $dspace;
                                    $val_tot = 0;
                                    $print_tot = false;
                                }
                            }
                            $last_key4 = $key4;
                        }
                    }
                }
            }
        }
    }
    $martext .= "\r\n " . fill_string("Total Qualified:", 72, ' ', 'left') . fill_string(($listing[$key]['maxqual'] + 0), 4, ' ', 'left') . "   " . fill_string(number_format(bcdiv($listing[$key]['maxqual'], $total_resps, 3) * 100, 2) . "%", 7, ' ', 'left') . "   " . number_format(bcdiv($listing[$key]['maxqual'], $total_resps, 3) * 100, 2) . "%\r\n";
    $martext .= "\r\n\r\n" . fill_string('_', 100, '_', 'left') . "\r\n\r\n";
    if (trim($saveas) == '') {
        $saveas = $project . ".MAR";
    }
    $tmpdate = date('m') . "/" . date('d') . "/" . date('Y');
    $martext = "Report created on $tmpdate\r\n\r\n" . $martext;
    if (is_file($proj_path . $saveas)) {
        unlink($proj_path . $saveas);
    }
    if ($tmpfile = fopen($proj_path . $saveas, 'w')) {
        if (fwrite($tmpfile, $martext)) {
            chmod($proj_path . $saveas, 0666);
        }
        echo "This marginal for $project has been saved as 'k:\\$saveas'\r\nClick <a href=\"Marginals.php\">here</a> to run another marginal.\r\n\r\n";
    } else {
        echo "Error saving 'k:\\$saveas'\r\n";
    }
    echo $martext;
    echo "\r\n</pre>\r\n";
}
include '/home/michael/public_html/.inc/foot.inc';
?>
