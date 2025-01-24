// register.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registration-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            // Don't prevent default submission here - let validateForm handle it
            console.log('Form submission attempted');
            
            // Log form data (excluding passwords)
            const formData = new FormData(form);
            console.log('Form data:');
            for (let pair of formData.entries()) {
                if (!pair[0].includes('password')) {
                    console.log(pair[0] + ': ' + pair[1]);
                }
            }
        });
    }
});

function validateForm() {
    // Get form values
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    var dob_day = document.getElementById('dob_day').value;
    var dob_month = document.getElementById('dob_month').value;
    var dob_year = document.getElementById('dob_year').value;

    // Validate required fields
    const form = document.getElementById('registration-form');
    const requiredFields = form.querySelectorAll('input[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value) {
            console.log(`Field ${field.name} is empty`);
            isValid = false;
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
    });

    // Check if passwords match
    if (password1 !== password2) {
        alert("Passwords do not match!");
        return false;
    }

    // Check if date is valid
    if (dob_day && dob_month && dob_year) {
        var date = new Date(dob_year, dob_month - 1, dob_day);
        var today = new Date();
        var age = today.getFullYear() - date.getFullYear();
        
        // Check if birthday hasn't occurred this year
        if (today.getMonth() < date.getMonth() || 
            (today.getMonth() === date.getMonth() && today.getDate() < date.getDate())) {
            age--;
        }

        if (age < 18) {
            alert("You must be 18 or over to register!");
            return false;
        }
    }

    // Validate user status
    const userStatus = form.querySelectorAll('input[name="user_status"]:checked');
    if (userStatus.length === 0) {
        console.log('No user status selected');
        alert('Please select at least one status option');
        return false;
    }

    if (!isValid) {
        console.log('Form validation failed');
        return false;
    }

    console.log('Form is valid, submitting...');
    return true;
}

// Gender field handling
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input[name="gender"]').forEach((elem) => {
        elem.addEventListener("change", function (event) {
            const otherInput = document.getElementById("gender_other");
            if (event.target.value === "other") {
                otherInput.style.display = "inline";
            } else {
                otherInput.style.display = "none";
                otherInput.value = "";
            }
        });
    });
});