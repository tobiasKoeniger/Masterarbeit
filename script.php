
<?php
$servername = "localhost";

$filepath = "/home/pi/Software/Masterarbeit/credentials.txt";

$lines = file($filepath);

$username = $lines[2];
$password = $lines[5];

$username = str_replace("\n", "", $username);
$password = str_replace("\n", "", $password);

echo "Username: " . $username . "\n";
echo "Password: " . $password . "\n\n";

//// Create connection
$conn = new mysqli($servername, $username, $password, "hydroponics");

// Check connection
if ($conn->connect_error) {
	$lines = "Error";
  // die("Connection failed: " . $conn->connect_error);
}
// echo "Connected successfully";

$sql = "SELECT time, temperature, humidity, lightIntensity, waterTemperature FROM sensors";

$result = $conn->query($sql);

$row = $result->fetch_assoc();

$row = json_encode($row);

echo $row;

$conn->close();

?>
