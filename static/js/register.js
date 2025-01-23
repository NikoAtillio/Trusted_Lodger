function validateForm() {
    // Get form values
    var password1 = document.getElementById('password1').value;
    var password2 = document.getElementById('password2').value;
    var dob_day = document.getElementById('dob_day').value;
    var dob_month = document.getElementById('dob_month').value;
    var dob_year = document.getElementById('dob_year').value;

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

    return true;
}