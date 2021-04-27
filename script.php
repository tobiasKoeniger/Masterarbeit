
<?php
$servername = "localhost";

$filepath = "/home/pi/Software/Masterarbeit/credentials.txt";

$lines = file($filepath);

$username = $lines[2];
$password = $lines[5];

echo $username;
echo $password;

//// Create connection
$conn = new mysqli($servername, $username, $password, "hydroponics");

// Check connection
if ($conn->connect_error) {
	$lines = "Error";
  // die("Connection failed: " . $conn->connect_error);
}
// echo "Connected successfully";

?>
