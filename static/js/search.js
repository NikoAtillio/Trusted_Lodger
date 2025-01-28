document.addEventListener('DOMContentLoaded', () => {
    let map;
    let marker;

    // Initialize the map
    function initMap() {
        const mapElement = document.getElementById('map');
        if (!mapElement) return;

        // Default to London coordinates
        const defaultLocation = { lat: 51.4545, lng: -2.5879 }; // Bristol coordinates
        
        // Create map
        map = new google.maps.Map(mapElement, {
            center: defaultLocation,
            zoom: 13,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: false,
            zoomControl: true,
            zoomControlOptions: {
                position: google.maps.ControlPosition.RIGHT_TOP
            }
        });

        // Create marker
        marker = new google.maps.Marker({
            map: map,
            position: defaultLocation,
            draggable: false,
            animation: google.maps.Animation.DROP
        });

        // Force map to redraw
        setTimeout(() => {
            google.maps.event.trigger(map, 'resize');
            map.setCenter(defaultLocation);
        }, 500);
    }

    // Initialize Autocomplete for both location inputs
    function initAutocomplete() {
        // Quick search location input
        const quickSearchInput = document.getElementById('location');
        if (quickSearchInput) {
            const autocomplete1 = new google.maps.places.Autocomplete(quickSearchInput, {
                componentRestrictions: { country: 'gb' }
            });
        }

        // Main search location input
        const mainSearchInput = document.getElementById('location-main');
        if (mainSearchInput) {
            const autocomplete2 = new google.maps.places.Autocomplete(mainSearchInput, {
                componentRestrictions: { country: 'gb' }
            });
            
            // Update map when location is selected
            autocomplete2.addListener('place_changed', () => {
                const place = autocomplete2.getPlace();
                if (place.geometry) {
                    const location = place.geometry.location;
                    map.setCenter(location);
                    marker.setPosition(location);
                    map.setZoom(14);
                }
            });
        }
    }

    // Geolocation functionality
    const getLocationButton = document.getElementById('get-location');
    const locationInput = document.getElementById('location');
    
    if (getLocationButton && locationInput) {
        getLocationButton.addEventListener('click', () => {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;

                        // Use Google Maps Geocoding API to get the location name
                        const geocoder = new google.maps.Geocoder();
                        const latlng = { lat: latitude, lng: longitude };

                        geocoder.geocode({ location: latlng }, (results, status) => {
                            if (status === 'OK' && results[0]) {
                                locationInput.value = results[0].formatted_address;
                                
                                // If map exists, update it
                                if (map && marker) {
                                    map.setCenter(latlng);
                                    marker.setPosition(latlng);
                                    map.setZoom(14);
                                }
                            } else {
                                alert('Unable to retrieve location. Please enter it manually.');
                            }
                        });
                    },
                    (error) => {
                        alert('Unable to retrieve your location. Please check your browser settings.');
                    }
                );
            } else {
                alert('Geolocation is not supported by this browser.');
            }
        });
    }

    // Wait for Google Maps to load then initialize
    if (typeof google === 'undefined') {
        console.error('Google Maps API is not loaded.');
        return;
    }

    // Initialize map and autocomplete
    try {
        initMap();
        initAutocomplete();
    } catch (error) {
        console.error('Error initializing map:', error);
    }
});