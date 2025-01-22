// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the button element
    const getLocationButton = document.getElementById('get-location');

    // Check if the button exists
    if (getLocationButton) {
        // Add a click event listener to the button
        getLocationButton.addEventListener('click', function() {
            console.log('Location button clicked'); // Debug log
            
            // Check if geolocation is supported
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    
                    console.log('Coordinates obtained:', { latitude, longitude }); // Debug log

                    // Use a reverse geocoding service to get the location name from coordinates
                    fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=en`)
                        .then(response => response.json())
                        .then(data => {
                            console.log('Geocoding response:', data); // Debug log
                            if (data.locality) {
                                document.getElementById('location').value = data.locality; // Fill the input with the locality
                                console.log('Location set to:', data.locality); // Debug log
                            } else {
                                console.log('No locality found in response'); // Debug log
                                alert('Location not found. Please enter it manually.');
                            }
                        })
                        .catch(error => {
                            console.error('Error fetching location:', error);
                            alert('Could not retrieve location. Please enter it manually.');
                        });
                }, function(error) {
                    console.error('Geolocation error:', error); // Debug log
                    alert('Unable to retrieve your location. Please check your browser settings.');
                });
            } else {
                console.log('Geolocation not supported'); // Debug log
                alert('Geolocation is not supported by this browser.');
            }
        });
    } else {
        console.warn('Button with ID "get-location" not found. Skipping geolocation functionality.');
    }
});