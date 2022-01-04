
<?php
	
	//
	$filepath = base64_decode("L2hvbWUvcGkvU29mdHdhcmUvTWFzdGVyYXJiZWl0L2NyZWRlbnRpYWxzLnR4dA==");

	$lines = file($filepath);

	$servername = $lines[2];
	$username = $lines[5];
	$password = $lines[8];

	// 
	$servername = str_replace("\n", "", $servername);
	$username = str_replace("\n", "", $username);
	$password = str_replace("\n", "", $password);

	// Create connection
	$conn = new mysqli($servername, $username, $password, "hydroponics");

	// Check connection
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	}
	// echo "Connected successfully";

	
	// 
	$message = file_get_contents('php://input');
	//echo $str_json;
	
	$firstPart = "UPDATE userInput SET time = NOW(), ";
	
	
	// 
	$sql = $firstPart . $message;
	
	// 
	if ($conn->query($sql) === TRUE) {
		echo "Record updated successfully: " . $message;
	} else {
		echo "Error updating record: " . $conn->error;
	}

	// 
	$conn->close();
  
?>
