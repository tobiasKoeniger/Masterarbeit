
<?php
	
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
		die("Connection failed: " . $conn->connect_error);
	}
	// echo "Connected successfully";
	
	//echo isset( $_POST["systemState"]);
		

	if ( isset( $_POST["systemState"]) ) {
		$sql = "UPDATE userInput SET time = NOW(), systemState = TRUE"; 
	}

	if ( isset( $_POST["systemState"]) === FALSE ){
		$sql = "UPDATE userInput SET time = NOW(), systemState = FALSE"; 
	}
	
	# save data to mysql database table hydroponics
	
	if ($conn->query($sql) === TRUE) {
		//echo "Record updated successfully";
	} else {
		echo "Error updating record: " . $conn->error;
	}

	$conn->close();
  
?>
