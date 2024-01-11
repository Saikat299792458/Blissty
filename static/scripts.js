
function captureImage() {
    const imageInput = document.getElementById('imageInput');
    const capturedImage = document.getElementById('capturedImage');
    const captureButton = document.getElementById('captureButton');

    // Display the captured image immediately after selection
    imageInput.addEventListener('change', function () {
        capturedImage.src = URL.createObjectURL(imageInput.files[0]);
        capturedImage.style.display = 'block';
        capturedImage.style.width = '100%';
        capturedImage.style.height = 'auto';

        // Change "Capture Image" button to "Recapture" button style
        captureButton.innerHTML = 'Recapture'

        // Hide result and Show the "Process Image" button
        document.getElementById('processButton').style.display = 'block';
        document.getElementById('result').style.display = 'none';
    });

    // Trigger a click on the file input
    imageInput.click();
}

function processImage() {
    // Check if the device model name is empty
    const modelName = document.getElementById('modelName').value.trim();
    if (modelName === '') {
        alert('Please enter the device model name.');
        return;
    }

    // Hide table and start loading
    document.getElementById('Loading').style.display = 'block';
    // Get form data
    const formData = new FormData(document.getElementById('imageForm'));

    // Send image to the server
    fetch('/process_image', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        // Update UI with processed data
        updateTable(data);
    })
    .catch(error => console.error('Error:', error));
}



function updateTable(data) {
    // Stop loading and show result
    document.getElementById('Loading').style.display = 'none';
    document.getElementById('result').style.display = 'block';
    const tableBody = document.getElementById('tableBody'); // Assuming you have a tbody with the id 'tableBody'

    // Clear existing rows
    tableBody.innerHTML = '';

    // Create a new row for each property in the processed data
    for (const key in data) {
        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${key}</td>
            <td>${data[key]}</td>
        `;

        // Append the new row to the table body
        tableBody.appendChild(newRow);
    }
}

