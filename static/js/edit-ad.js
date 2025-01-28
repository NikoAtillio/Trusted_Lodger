// static/js/edit-ad.js

// Global variables
let map, marker;

// Load Google Maps API programmatically
function loadGoogleMapsAPI() {
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${googleMapsApiKey}&libraries=places`;
    script.async = true;
    script.defer = true;
    script.onload = initMap;
    document.head.appendChild(script);
}

function initMap() {
    // Get form inputs
    const locationInput = document.getElementById('location');
    const postcodeInput = document.getElementById('postcode');
    const defaultLocation = { lat: 51.5074, lng: -0.1278 }; // London

    const mapOptions = {
        zoom: 13,
        center: defaultLocation,
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false,
        zoomControl: true,
        styles: [
            {
                featureType: "poi",
                elementType: "labels",
                stylers: [{ visibility: "off" }]
            }
        ]
    };

    // Initialize map
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    marker = new google.maps.Marker({
        map: map,
        position: defaultLocation,
        draggable: true
    });

    // Initialize Places Autocomplete
    const autocomplete = new google.maps.places.Autocomplete(locationInput, {
        componentRestrictions: { country: "uk" }
    });

    autocomplete.bindTo('bounds', map);

    // Handle place selection
    autocomplete.addListener('place_changed', function() {
        const place = autocomplete.getPlace();
        if (!place.geometry) return;

        map.setCenter(place.geometry.location);
        map.setZoom(15);
        marker.setPosition(place.geometry.location);

        // Update postcode if available
        const postcode = place.address_components.find(component =>
            component.types.includes('postal_code')
        );
        if (postcode) {
            postcodeInput.value = postcode.long_name;
        }
    });

    // If there's an existing location, geocode it
    if (locationInput.value) {
        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ 
            address: locationInput.value + ', UK' 
        }, function(results, status) {
            if (status === 'OK' && results[0]) {
                const location = results[0].geometry.location;
                map.setCenter(location);
                map.setZoom(15);
                marker.setPosition(location);
            }
        });
    }

    // Update address when marker is dragged
    marker.addListener('dragend', function() {
        const position = marker.getPosition();
        const geocoder = new google.maps.Geocoder();
        
        geocoder.geocode({
            location: { lat: position.lat(), lng: position.lng() }
        }, function(results, status) {
            if (status === 'OK' && results[0]) {
                locationInput.value = results[0].formatted_address;
                
                const postcode = results[0].address_components.find(component =>
                    component.types.includes('postal_code')
                );
                if (postcode) {
                    postcodeInput.value = postcode.long_name;
                }
            }
        });
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
document.addEventListener('DOMContentLoaded', loadGoogleMapsAPI);

// Export functions for global access
window.validateForm = validateForm;

// In edit-ad.js, update the validateForm function:
function validateForm() {
    const requiredFields = document.querySelectorAll('[required]');
    let isValid = true;

    // Log form data for debugging
    const formData = new FormData(document.querySelector('form'));
    console.log('Form data:');
    for (let pair of formData.entries()) {
        console.log(pair[0] + ': ' + pair[1]);
    }

    requiredFields.forEach(field => {
        if (!field.value) {
            field.style.borderColor = 'red';
            isValid = false;
            console.log('Empty required field:', field.id || field.name);
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