// Google Maps Integration
let map, marker;

function initMap() {
    const defaultLocation = { lat: 51.5074, lng: -0.1278 }; // London
    
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13,
        center: defaultLocation
    });

    marker = new google.maps.Marker({
        map: map,
        position: defaultLocation,
        draggable: true
    });

    // Location autocomplete
    const input = document.getElementById('location');
    const autocomplete = new google.maps.places.Autocomplete(input);
    
    autocomplete.addListener('place_changed', function() {
        const place = autocomplete.getPlace();
        if (!place.geometry) return;

        map.setCenter(place.geometry.location);
        marker.setPosition(place.geometry.location);
        
        // Update hidden fields with coordinates
        document.getElementById('lat').value = place.geometry.location.lat();
        document.getElementById('lng').value = place.geometry.location.lng();
    });
}

// Form validation
function validateForm() {
    const requiredFields = document.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value) {
            field.style.borderColor = 'red';
            isValid = false;
        } else {
            field.style.borderColor = '#ccc';
        }
    });

    if (!isValid) {
        alert('Please fill in all required fields');
        return false;
    }

    const minAge = parseInt(document.getElementById('min_age').value);
    const maxAge = parseInt(document.getElementById('max_age').value);
    if (minAge > maxAge) {
        alert('Minimum age cannot be greater than maximum age');
        return false;
    }

    return true;
}

// Initialize everything when the page loads
document.addEventListener('DOMContentLoaded', function() {
    // Google Maps script will call initMap automatically
});