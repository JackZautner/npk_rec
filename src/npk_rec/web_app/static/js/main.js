$(document).ready(function() {
    // Debug
    console.log('JavaScript loaded');
    console.log('jQuery version: ', $.fn.jquery);
    $('#myTable').DataTable();

    // Event listener for .aws-fetch
    $(document).on('click', '.aws-fetch', function() {
        const plant = $(this).closest('tr').find('.plant-dropdown').val(); // Get the selected dropdown value
        const rowId = $(this).data('id');
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
                // Update the "Ideal NPK Ratio" column for the corresponding plant
                const idealNpkCell = $(`.ideal-npk[data-id="${data.plant_id}"]`);
                const actualNpkCell = $(`.actual-npk[data-id="${data.plant_id}"]`);
                idealNpkCell.text(data.optimal_npk); // Update the cell's text with the fetched value
                actualNpkCell.text(data.actual_npk)
            } else {
                alert(data.error || 'Error fetching data');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Event listener for change in .plant-dropdown
    $(document).on('change', '.plant-dropdown', function() {
        const newPlant = $(this).val(); // New dropdown value
        const rowId = $(this).data('id'); // Get row ID

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