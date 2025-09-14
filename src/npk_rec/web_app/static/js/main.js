$(document).ready(function() {
    // Debug
    console.log('JavaScript loaded');
    console.log('jQuery version: ', $.fn.jquery);
    $('#myTable').DataTable();

    // Event listener for .aws-fetch
    $(document).on('click', '.aws-fetch', function() {
        const plant = $('#plant-select').val(); // Get the selected plant from the dropdown
        const rowId = $(this).data('id');
        console.log(`Fetching data for plant: ${plant}, row ID: ${rowId}`);
        fetch('/api/fetch_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ plant: plant, id: rowId }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.optimal_npk) {
                // Update the "Ideal NPK Ratio" and "Actual NPK Ratio" for the single plant
                $('.ideal-npk').text(data.optimal_npk);
                $('.actual-npk').text(data.actual_npk);
            } else {
                alert(data.error || 'Error fetching data');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Event listener for change in .plant-dropdown
    $(document).on('change', '#plant-select', function() {
        const newPlant = $(this).val(); // New dropdown value
        const rowId = $('.aws-fetch').data('id'); // Get row ID from the fetch button

        // Send updated value to the backend
        fetch('/api/update_dropdown', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id: rowId, plant: newPlant }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log(`Updated plant to ${newPlant} for row ${rowId}`);
            } else {
                alert(data.error || 'Error updating dropdown value');
            }
        })
        .catch(error => console.error('Error: ', error));
    });
});