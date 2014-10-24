<?
	$actions = "rush,drop,mass";
	$units = "scvs,marines,marauders,reapers,ghosts,siege tanks,hellions,thors,vikings,medivacs,banshees,ravens,battlecruisers,turrets,";
	$units .= "probes,zealots,stalkers,sentries,high templars,dark templars,immortals,colossuses,void rays,phoenixes,carriers,cannons,motherships,";
	$units .= "drones,zerglings,banelings,roaches,hydralisks,mutalisks,corruptors,infestors,queens,brood lords,ultralisks,spore crawlers,spine crawlers";
	$actions = explode(",",$actions);
	$units = explode(",", $units);
	shuffle($actions);
	shuffle($units);
	print $actions[0] . " " . $units[0];
?>
