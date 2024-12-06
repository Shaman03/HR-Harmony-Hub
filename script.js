function signIn() {
    // Simulate a sign-in process or redirect
    const userConfirmed = confirm("Would you like to proceed to the sign-in page?");
    if (userConfirmed) {
        // Example: Redirecting to a login page
        window.location.href = "login.html";
    } else {
        alert("Sign-in canceled.");
    }
}
