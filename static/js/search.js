document.addEventListener('DOMContentLoaded', function () {
    const getLocationButton = document.getElementById('get-location');
    const locationInput = document.getElementById('location-main');

    // Initialize Google Maps Places Autocomplete
    const autocomplete = new google.maps.places.Autocomplete(locationInput, {
        types: ['(cities)'],
        componentRestrictions: { country: 'uk' },
    });

    if (getLocationButton) {
        getLocationButton.addEventListener('click', function () {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function (position) {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;

                        // Use Google Maps Geocoding API to get the location name
                        const geocoder = new google.maps.Geocoder();
                        const latlng = { lat: latitude, lng: longitude };

                        geocoder.geocode({ location: latlng }, function (results, status) {
                            if (status === 'OK' && results[0]) {
                                locationInput.value = results[0].formatted_address;
                            } else {
                                alert('Unable to retrieve location. Please enter it manually.');
                            }
                        });
                    },
                    function (error) {
                        alert('Unable to retrieve your location. Please check your browser settings.');
                    }
                );
            } else {
                alert('Geolocation is not supported by this browser.');
            }
        });
    }
});