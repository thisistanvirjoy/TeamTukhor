// Create a Leaflet map
const map = L.map('map').setView([0, 0], 2); // Set the initial view

// Add a base map layer (e.g., OpenStreetMap)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Load your CSV data (adjust the path to your CSV file)
d3.csv('new.csv').then(data => {
    // Create a GeoJSON FeatureCollection to store area features
    const geoJsonFeatures = [];

    data.forEach(row => {
        // Extract latitude and longitude values from CSV data
        const latitude = parseFloat(row.latitude);
        const longitude = parseFloat(row.longitude);

        // Check if latitude and longitude are valid numbers
        if (!isNaN(latitude) && !isNaN(longitude)) {
            // Create a GeoJSON feature for each data point
// Create a GeoJSON feature for each data point
const feature = {
    type: 'Feature',
    geometry: {
        type: 'Point',
        coordinates: [longitude, latitude]
    },
    properties: {
        // You can customize the properties here, e.g., color and data value
        color: getColorBasedOnData(row),
        dataValue: row.some_data_column, // Assuming this is the data value column name
        dataValue2: row.soil_moisture, // Corrected the property name
        dataValue3: row.rainfall,
    }
};


            geoJsonFeatures.push(feature);
        }
    });

    // Create a GeoJSON FeatureCollection from the features
    const geoJsonData = {
        type: 'FeatureCollection',
        features: geoJsonFeatures
    };

// Add the GeoJSON data as a GeoJSON layer to the map
L.geoJSON(geoJsonData, {
    pointToLayer: function (feature, latlng) {
        // Customize the marker icon based on properties (e.g., color)
        const marker = L.circleMarker(latlng, {
            radius: 6,
            fillColor: feature.properties.color,
            color: 'black',
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8
        });

        // Add a popup to the marker showing both data values
        marker.bindPopup(`Tree Canopy: ${feature.properties.dataValue}<br>Soil Moisture: ${feature.properties.dataValue2}<br>Rain Fall: ${feature.properties.dataValue3}`);

        return marker;
    }
}).addTo(map);

}).catch(error => {
    console.error('Error loading CSV data:', error);
});

// Define a function to get a color based on your data (customize as needed)
function getColorBasedOnData(row) {
    // Example: Return a color based on a specific column value
    const value = parseFloat(row.some_data_column);
    if (!isNaN(value)) {
        if (value < 0.3) {
            return 'red';
        } else if (value < 0.6) {
            return 'yellow';
        } else {
            return 'green';
        }
    }
    return 'gray'; // Default color if data is not available or doesn't match conditions
}
