document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    const navbar = document.querySelector('.navbar');
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

    const userIcon = document.getElementById('user-icon');
    const dropdownContent = document.getElementById('dropdown-content');

    if (userIcon && dropdownContent) {
        userIcon.addEventListener('click', function() {
            dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
        });
    }

    // Close the dropdown if the user clicks outside of it
    window.addEventListener('click', function(event) {
        if (!event.target.matches('#user-icon')) {
            if (dropdownContent.style.display === 'block') {
                dropdownContent.style.display = 'none';
            }
        }
    });
});
