// Select the drop zone and file input elements
const dropZone = document.getElementById('drop_zone');
const fileInput = document.getElementById('file_input');

// Handle file drop
dropZone.addEventListener('dragover', (event) => {
    event.preventDefault();
    dropZone.classList.add('dragover');
    dropZone.textContent = "Release to Upload";
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
    dropZone.textContent = "Drag files here";
});

dropZone.addEventListener('drop', (event) => {
    event.preventDefault();
    dropZone.classList.remove('dragover');
    dropZone.textContent = "Uploading...";
    
    // Get the dropped file
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        //fileInput.files = files;

        // Automatically submit the form once the file is dropped
        const formData = new FormData();
        //formData.append('file', files[0]);
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }
        
        // Send the file to the server using Fetch API
        fetch("{{ url_for('upload_file') }}", {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(result => {
            dropZone.textContent = result;
        })
        .catch(error => {
            dropZone.textContent = "Error uploading file";
        });
    }
});