<?php

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "`user register`"; //

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Assuming form data is sent via POST
$username = $_POST['username'];
$email = $_POST['email'];
$password = $_POST['password'];  // You should hash the password in production

$sql = "INSERT INTO `users` (username, email, password) VALUES ('$username', '$email', '$password')";

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();


?>