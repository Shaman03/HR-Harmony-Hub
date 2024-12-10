
document.addEventListener("DOMContentLoaded", function() {
    // 1. Handle form submission for profile updates
    const profileForm = document.getElementById("profileForm");
    if (profileForm) {
        profileForm.addEventListener("submit", function(event) {
            event.preventDefault(); // Prevent the default form submission

            const formData = new FormData(profileForm); // Collect form data

            // Send form data to Flask backend
            fetch('/save_user_profile', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.text())  // Expecting a text response
            .then(data => {
                alert(data); // Show backend response message
                if (data === 'User profile updated successfully.') {
                    window.location.reload(); // Reload the page to show updated info
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while saving the profile.');
            });
        });
    }

    // 2. Display user info when "Show Info" button is clicked
    window.displayInfo = function() {
        fetch('/display_info')  // GET request to get user info from backend
            .then(response => response.json())  // Expecting JSON data
            .then(data => {
                if (data.error) {
                    alert(data.error);  // Show error message
                } else {
                    // Construct a table to display the user's info
                    const infoHtml = `
                        <table class="table">
                            <tr><th>Name</th><td>${data.name}</td></tr>
                            <tr><th>Email</th><td>${data.email}</td></tr>
                            <tr><th>Department</th><td>${data.department}</td></tr>
                            <tr><th>Job Title</th><td>${data.job_title}</td></tr>
                            <tr><th>Phone Number</th><td>${data.phone_number}</td></tr>
                            <tr><th>Address</th><td>${data.address}</td></tr>
                            <tr><th>Salary</th><td>${data.salary}</td></tr>
                            <tr><th>CV Filename</th><td>${data.cv_filename}</td></tr>
                        </table>
                    `;
                    document.getElementById('infoPopup').innerHTML = infoHtml; // Insert into the popup div
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Failed to fetch user info.');
            });
    };
});
