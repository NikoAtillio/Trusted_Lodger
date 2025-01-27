// register.js
console.log('register.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded');
    
    const form = document.getElementById('registration-form');
    console.log('Form found:', !!form);

    if (form) {
        // Form submission handler
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            console.log('Form submission attempted');
            
            if (validateForm()) {
                console.log('Form validation passed, submitting...');
                this.submit();
            } else {
                console.log('Form validation failed');
            }
        });

        // Gender field handling
        document.querySelectorAll('input[name="gender"]').forEach((elem) => {
            elem.addEventListener("change", function(event) {
                const otherInput = document.getElementById("gender_other");
                if (otherInput) {
                    otherInput.style.display = event.target.value === "other" ? "inline" : "none";
                    if (event.target.value !== "other") {
                        otherInput.value = "";
                    }
                }
            });
        });
    }
});

function validateForm() {
    console.log('Validation started');
    let isValid = true;

    // Get form elements
    const form = document.getElementById('registration-form');
    const password1 = document.getElementById('password1')?.value;
    const password2 = document.getElementById('password2')?.value;
    const dobDay = document.getElementById('dob_day')?.value;
    const dobMonth = document.getElementById('dob_month')?.value;
    const dobYear = document.getElementById('dob_year')?.value;

    // Validate required fields
    const requiredFields = [
        'first_name', 'last_name', 'email', 
        'password1', 'password2', 'dob_day', 
        'dob_month', 'dob_year'
    ];

    requiredFields.forEach(fieldName => {
        const field = document.getElementById(fieldName);
        if (field) {
            if (!field.value) {
                console.log(`Missing required field: ${fieldName}`);
                field.classList.add('error');
                isValid = false;
            } else {
                field.classList.remove('error');
            }
        }
    });

    // Password validation
    if (password1 !== password2) {
        alert("Passwords do not match!");
        isValid = false;
    }

    // Age validation
    if (dobDay && dobMonth && dobYear) {
        const date = new Date(dobYear, dobMonth - 1, dobDay);
        const today = new Date();
        let age = today.getFullYear() - date.getFullYear();
        
        if (today.getMonth() < date.getMonth() || 
            (today.getMonth() === date.getMonth() && today.getDate() < date.getDate())) {
            age--;
        }

        if (age < 18) {
            alert("You must be 18 or over to register!");
            isValid = false;
        }
    }

    // User status validation
    const userStatus = form.querySelectorAll('input[name="user_status"]:checked');
    if (userStatus.length === 0) {
        console.log('No user status selected');
        alert('Please select at least one status option');
        isValid = false;
    }

    // Log form data (excluding passwords)
    if (isValid) {
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            if (!key.includes('password')) {
                data[key] = value;
            } else {
                data[key] = '[HIDDEN]';
            }
        });
        console.log('Form data:', data);
    }

    return isValid;
}