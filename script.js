function displayInfo() {
    fetch('/display_info')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user info.');
            }
            return response.json();
        })
        .then(data => {
            console.log('User info retrieved:', data); // Debugging output
            const infoPopup = document.getElementById('infoPopup');
            infoPopup.innerHTML = `
                <button class="close-btn" onclick="closePopup()">×</button>
                <h5>Employee Details:</h5>
                <p>Department: ${data.department || "N/A"}</p>
                <p>Job Title: ${data.job_title || "N/A"}</p>
                <p>Phone Number: ${data.phone_number || "N/A"}</p>
                <p>Address: ${data.address || "N/A"}</p>
                <p>Salary: ${data.salary || "N/A"}</p>
                <p> CV name: ${data.cv_filename || "N/A"} </p>
            `;
            infoPopup.classList.add('show');
        })
        .catch(err => {
            console.error('Error fetching user info:', err);
        });
}
