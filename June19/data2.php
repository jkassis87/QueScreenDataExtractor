<?php
/**
 * filename: data.php
 * description: this will return the requested stats
 */

//setting header to json
//header('Content-Type: application/json');

//database
define('DB_HOST', '127.0.0.1');
define('DB_USERNAME', 'larauser');
define('DB_PASSWORD', 'password');
define('DB_NAME', 'charta');

//get connection
$mysqli = new mysqli(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_NAME);
if(!$mysqli){
	die("Connection failed: " . $mysqli->error);
}

// set the _GET values
$brand = $_GET["brand"];
$tstamp = $_GET["date"];

if ($brand == 'ALL') {

	$qDP = "SELECT Stat, Tstamp FROM alldata WHERE Brand = 'DP' AND Tstamp Like '$tstamp' ORDER BY Tstamp ASC";
	$rDP = $mysqli->query($qDP);
	print_r($rDP);
	$dDP = array();
	foreach ($rDP as $row) { $dDP[] = $row; }

	$qPA = "SELECT Stat, Tstamp FROM alldata WHERE Brand = 'PA' AND Tstamp Like '$tstamp' ORDER BY Tstamp ASC";
	$rPA = $mysqli->query($qPA);
	$dPA = array();
	foreach ($rPA as $row) { $dPA[] = $row; }

	$qCR = "SELECT Stat, Tstamp FROM alldata WHERE Brand = 'CR' AND Tstamp Like '$tstamp' ORDER BY Tstamp ASC";
	$rCR = $mysqli->query($qCR);
	$dCR = array();
	foreach ($rCR as $row) { $dCR[] = $row; }

	$data = array();
	foreach (array_keys($dDP + $dPA + $dCR) as $key) {
		$comb[$key] = $dDP[$key] + $dPA[$key] + $dCR[$key];
	}

} else {
	
	$query = "SELECT Stat, Tstamp FROM alldata WHERE Brand = '$brand' AND Tstamp Like '$tstamp' ORDER BY Tstamp ASC";
	$result = $mysqli->query($query);
	$data = array();
	foreach ($result as $row) { $data[] = $row; } 

}



//now print the data
//echo json_encode($data);
var_dump($data);