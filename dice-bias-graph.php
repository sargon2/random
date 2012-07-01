<?php
chdir("/home/sargon/xem/random/jpgraph/jpgraph-2.1.4/src/Examples");
// $Id: barscalecallbackex1.php,v 1.2 2002/07/11 23:27:28 aditus Exp $
include ("../jpgraph.php");
include ("../jpgraph_bar.php");

$datay = explode(",", $datay);

// Create the graph and setup the basic parameters 
$graph = new Graph(600,300,'auto');
$graph->img->SetMargin(40,30,30,40);
$graph->SetScale("linlin");
$graph->SetShadow();
$graph->SetFrame(false); // No border around the graph

// Create a bar pot
$bplot = new BarPlot($datay);
$bplot->SetFillColor("blue");
$bplot->SetWidth(0.5);
$bplot->SetShadow();
$graph->xaxis->SetTickLabels(array(2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12));

// Setup the values that are displayed on top of each bar
$bplot->value->Show();
$bplot->value->SetFormat('%0.3f%%');
// Black color for positive values and darkred for negative values
$bplot->value->SetColor("black","darkred");
$graph->Add($bplot);

// Finally stroke the graph
$graph->Stroke();
?>
