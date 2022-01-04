
<?php

	header('Content-Type: text/event-stream');
	header('Cache-Control: no-cache');


	$filepath = base64_decode("L2hvbWUvcGkvU29mdHdhcmUvTWFzdGVyYXJiZWl0L2NyZWRlbnRpYWxzLnR4dA==");

	$lines = file($filepath);

	$servername = $lines[2];
	$username = $lines[5];
	$password = $lines[8];

	$servername = str_replace("\n", "", $servername);
	$username = str_replace("\n", "", $username);
	$password = str_replace("\n", "", $password);

	//// Create connection
	$conn = new mysqli($servername, $username, $password, "hydroponics");

	// Check connection
	if ($conn->connect_error) {
		$lines = "Error";
		die("Connection failed: " . $conn->connect_error);
	}
	// echo "Connected successfully";


	$sql = "SELECT time, temperature, humidity, lightIntensity, waterTemperature FROM sensors";

	$result = $conn->query($sql);

	$sql = "SELECT time, temperature, humidity, lightIntensity, waterTemperature FROM sensors";

	$result = $conn->query($sql);

	// convert to array
	$row = $result->fetch_assoc();

	// convert to json
	$row = json_encode($row);

	//$time = date('r');

	echo "retry: 1000\n";
	echo "data: {$row}\n\n";

	flush();

	$conn->close();

?>
