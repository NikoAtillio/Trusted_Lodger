document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap initialization (only if Bootstrap is loaded)
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // Navbar scroll behavior
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        let lastScrollTop = 0;
        window.addEventListener('scroll', function() {
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            if (scrollTop > lastScrollTop) {
                navbar.classList.add('hidden');
            } else {
                navbar.classList.remove('hidden');
            }
            lastScrollTop = scrollTop;
        });
    }

    // User dropdown functionality
    const userIcon = document.getElementById('user-icon');
    const dropdownContent = document.getElementById('dropdown-content');

    if (userIcon && dropdownContent) {
        userIcon.addEventListener('click', function(event) {
            event.stopPropagation();
            dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(event) {
            if (!dropdownContent.contains(event.target) && event.target !== userIcon) {
                dropdownContent.style.display = 'none';
            }
        });
    }

    // Initialize date of birth dropdowns
    initializeDateOfBirth();

    // Add form submission debugging
    const registrationForm = document.querySelector('form');
    if (registrationForm) {
        registrationForm.addEventListener('submit', function(e) {
            console.log('Form submission attempted');
            
            // Log form data
            const formData = new FormData(this);
            for (let pair of formData.entries()) {
                console.log(pair[0] + ': ' + pair[1]);
            }

            // Log the form's action attribute
            console.log('Form action:', this.action);
            console.log('Form method:', this.method);
            
            // Log any validation errors
            const invalidFields = this.querySelectorAll(':invalid');
            if (invalidFields.length > 0) {
                console.log('Invalid fields found:', invalidFields);
                invalidFields.forEach(field => {
                    console.log('Invalid field:', field.name, 'Validation message:', field.validationMessage);
                });
            }
        });
    }
});

// Function to initialize date of birth dropdowns
function initializeDateOfBirth() {
    const daySelect = document.querySelector('select[name="dob_day"]');
    const monthSelect = document.querySelector('select[name="dob_month"]');
    const yearSelect = document.querySelector('select[name="dob_year"]');

    if (daySelect && monthSelect && yearSelect) {
        // Generate days
        for (let i = 1; i <= 31; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i.toString().padStart(2, '0');
            daySelect.appendChild(option);
        }

        // Generate months
        const months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ];
        months.forEach((month, index) => {
            const option = document.createElement('option');
            option.value = index + 1;
            option.textContent = month;
            monthSelect.appendChild(option);
        });

        // Generate years (from current year - 100 to current year - 18)
        const currentYear = new Date().getFullYear();
        for (let year = currentYear - 18; year >= currentYear - 100; year--) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearSelect.appendChild(option);
        }
    }
}

// Form validation function with debugging
function validateForm() {
    console.log('validateForm() called');
    const checkboxes = document.querySelectorAll('input[name="user_status"]');
    const errorElement = document.getElementById("status-error");
    let isChecked = false;
    
    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            isChecked = true;
        }
    });
    
    console.log('Checkbox validation result:', isChecked);
    
    if (!isChecked) {
        errorElement.style.display = "block";
        console.log('Form validation failed: no checkbox selected');
        return false;
    }
    
    errorElement.style.display = "none";
    console.log('Form validation passed');
    return true;
}