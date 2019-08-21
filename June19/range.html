<?php
/**
 * filename: data.php
 * description: this will return the requested stats
 */

//setting header to json
header('Content-Type: application/json');

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
$sdate = $_GET["sdate"];
$edate = $_GET["edate"];

if ($brand == 'ALL') {

	$query = "SELECT Tstamp, SUM(Stat) as 'Stat' FROM alldata WHERE Date(Tstamp) BETWEEN '$sdate' and '$edate' GROUP BY Tstamp ORDER BY Tstamp ASC"; 
	$result = $mysqli->query($query);
	$data = array();
	foreach ($result as $row) { $data[] = $row; }

} else {
	
	$query = "SELECT Tstamp, SUM(Stat) as 'Stat' FROM alldata WHERE Date(Tstamp) BETWEEN '$sdate' and '$edate' AND Brand = '$brand' GROUP BY Tstamp ORDER BY Tstamp ASC"; 
	$result = $mysqli->query($query);
	$data = array();
	foreach ($result as $row) { $data[] = $row; } 

}

//now print the data
echo json_encode($data);
//echo json_encode($newArr);
//var_dump($data);
