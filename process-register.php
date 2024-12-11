<?php
// Database connection settings
$servername = "localhost";
$username = "root";
$password = "";  // Default XAMPP MySQL password
$dbname = "user_register";  // Your database name

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Get the form data
    $username = $_POST['username'];
    $email = $_POST['email'];
    $password = $_POST['password'];  // Plain-text password from form
    $password1 = $_POST['password1']; // Confirm password from form

    // Check if passwords match
    if ($password === $password1) {
        // Hash the password before storing
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);

        // Prepare the SQL statement
        $stmt = $conn->prepare("INSERT INTO users (username, email, password) VALUES (?, ?, ?)");
        $stmt->bind_param("sss", $username, $email, $hashed_password);

        // Execute the statement and check if successful
        if ($stmt->execute()) {
            echo "New record created successfully!";
        } else {
            echo "Error: " . $stmt->error;
        }

        // Close the prepared statement
        $stmt->close();
    } else {
        echo "Passwords do not match!";
    }
}

// Close the database connection
$conn->close();
?>
