document.getElementById('get-location').addEventListener('click', function() {
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