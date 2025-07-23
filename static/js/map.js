function initMap(latitude, longitude) {
    var map = L.map('map').setView([latitude, longitude], 13);

    // Load OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Set marker at user's current location
    var marker = L.marker([latitude, longitude]).addTo(map)
        .bindPopup('You are here.')
        .openPopup();

        
}

