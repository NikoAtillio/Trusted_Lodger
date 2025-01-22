// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the button element
    const getLocationButton = document.getElementById('get-location');

    // Check if the button exists
    if (getLocationButton) {
        // Add a click event listener to the button
        getLocationButton.addEventListener('click', function() {
            // Check if geolocation is supported
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    // Use a reverse geocoding service to get the location name from coordinates
                    fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.locality) {
                                document.getElementById('location').value = data.locality; // Fill the input with the locality
                            } else {
                                alert('Location not found. Please enter it manually.');
                            }
                        })
                        .catch(error => {
                            console.error('Error fetching location:', error);
                            alert('Could not retrieve location. Please enter it manually.');
                        });
                }, function() {
                    alert('Unable to retrieve your location. Please check your browser settings.');
                });
            } else {
                alert('Geolocation is not supported by this browser.');
            }
        });
    } else {
        console.warn('Button with ID "get-location" not found. Skipping geolocation functionality.');
    }
});