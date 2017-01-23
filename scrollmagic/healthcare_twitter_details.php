<?php
	$name = $_GET["twitter"];	
	$aca = $_GET["aca"];	
	$oc = $_GET["oc"];
	$party = $_GET["party"];		
?>

<h1>Tweets from <?php echo $name ?></h1>
<h3>Party - <?php echo $party ?>
<br>Number of ACA mentions - <?php echo $aca ?>
<br>Number of Obama Care mentions - <?php echo $oc ?> </h3>

<?php
$fileName = "data/aca_obamacare_details.csv";
ini_set('auto_detect_line_endings', true);


$file = fopen($fileName, 'r');
$tweets = array();
while (($line = fgetcsv($file)) !== FALSE) {
	

	if ( $line[7] == $name ) {
		$day = $line[1];
		if (strlen($day) == 1) {
			$day = "0" . $day;
		}
		$sortable_date = $line[8] . "-" . date('m',strtotime($line[2])) . "-" . $day;
		$readable_date = $line[2] . " " . $line[1] . ", " . $line[8];
		$tweet = preg_replace( '/[^[:print:]]/', '',$line[6]);
		$url = "https://twitter.com/" . $name . "/status/" . $line[9];

		$tweets[] = array($sortable_date, $readable_date, $tweet, $url);
   	}
   	
}
fclose($file);

function cmp($a, $b)
{
    if ($a == $b) {
        return 0;
    }
    return ($a[0] > $b[0]) ? -1 : 1;
}

usort($tweets, "cmp");
foreach ($tweets as $tweet) {
	echo $tweet[1] . " - <a href=\"" . $tweet[3] . "\">" . $tweet[2] . "</a><br>";
}

?>