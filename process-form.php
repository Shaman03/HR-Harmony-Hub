<?php
// Database connection settings
$servername = "localhost"; // Default XAMPP server
$username = "root"; // Default XAMPP MySQL user
$password = ""; // No password by default in XAMPP
$database = "hr harmony hub"; // Replace with your database name

// Connect to the database
$conn = new mysqli($servername, $username, $password, $database);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Get form inputs
    $department = $_POST["department"];
    $job_title = $_POST["job_title"];
    $phone_number = $_POST["phone_number"];
    $address = $_POST["address"];
    $salary = $_POST["salary"];

    // Handle the uploaded CV file
    if (isset($_FILES["file"]) && $_FILES["file"]["error"] === UPLOAD_ERR_OK) {
        $uploadDir = "uploads/"; // Directory to store uploaded files
        $cvFilename = basename($_FILES["file"]["name"]);
        $uploadFile = $uploadDir . $cvFilename;

        // Create the uploads directory if it doesn't exist
        if (!is_dir($uploadDir)) {
            mkdir($uploadDir, 0777, true);
        }

        // Move the uploaded file
        if (!move_uploaded_file($_FILES["file"]["tmp_name"], $uploadFile)) {
            die("Error uploading file.");
        }
    } else {
        $cvFilename = null; // No file uploaded
    }

    // Insert data into the database
    $stmt = $conn->prepare("INSERT INTO users (department, job_title, phone_number, address, salary, cv_filename) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("ssssds", $department, $job_title, $phone_number, $address, $salary, $cvFilename);

    if ($stmt->execute()) {
        echo "Profile saved successfully!";
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
}

// Close the database connection
$conn->close();

<?php

$servername = "localhost";
$username = "root";
$password = "";
$dbname = "`user register`"; // Make sure to use backticks for database name

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
