document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('upload-btn');
    const dropdownMenu = document.getElementById('dropdown-menu');
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    const fileInput = document.getElementById('file-input');
    const textArea = document.getElementById('text-area');
    const warningMessage = document.getElementById('warning-message');
    const submitBtn = document.getElementById('submit-btn');

    // Toggle dropdown menu visibility
    uploadBtn.addEventListener('click', () => {
        dropdownMenu.classList.toggle('show');
    });

    // Close dropdown if user clicks outside of it
    window.addEventListener('click', (event) => {
        if (!event.target.matches('#upload-btn')) {
            if (dropdownMenu.classList.contains('show')) {
                dropdownMenu.classList.remove('show');
            }
        }
    });

    // Handle dropdown item clicks
    dropdownItems.forEach(item => {
        item.addEventListener('click', (event) => {
            event.preventDefault();

            // Reset inputs and hide elements
            fileInput.style.display = 'none';
            fileInput.value = '';
            textArea.style.display = 'none';
            textArea.value = '';
            warningMessage.style.display = 'none';
            submitBtn.style.display = 'none';

            const method = item.getAttribute('data-method');

            if (method === 'file') {
                const fileType = item.getAttribute('data-file-type');
                fileInput.setAttribute('accept', fileType);
                fileInput.style.display = 'block';
                fileInput.click();

                if (fileType.includes('.pdf')) {
                    warningMessage.textContent = 'Warning: Pages should be less than 6.';
                    warningMessage.style.display = 'block';
                } else if (fileType.includes('.jpg')) {
                    warningMessage.textContent = 'Warning: Image size should be less than 10MB.';
                    warningMessage.style.display = 'block';
                } else {
                    warningMessage.textContent = '';
                }

                fileInput.addEventListener('change', () => {
                    if (fileInput.files.length > 0) {
                        submitBtn.style.display = 'block';
                    } else {
                        submitBtn.style.display = 'none';
                    }
                }, { once: true }); // Use {once: true} to prevent multiple listeners
            } else if (method === 'text') {
                textArea.style.display = 'block';
                warningMessage.textContent = 'Text area is preferred for faster conversion.';
                warningMessage.style.display = 'block';
                textArea.focus();
            }

            dropdownMenu.classList.remove('show');
        });
    });

    // Show submit button when text is entered
    textArea.addEventListener('input', () => {
        if (textArea.value.trim().length > 0) {
            submitBtn.style.display = 'block';
        } else {
            submitBtn.style.display = 'none';
        }
    });

    // Handle form submission
    document.getElementById('upload-form').addEventListener('submit', (event) => {
        // Prevent default form submission for demonstration
        event.preventDefault();
        
        // This is where you would handle the form data.
        // For a real-world application, you would use FormData and fetch API
        // to send the data to a backend server.
        
        if (fileInput.files.length > 0) {
            console.log('File submitted:', fileInput.files[0].name);
            // Example: const formData = new FormData(); formData.append('file', fileInput.files[0]);
        } else if (textArea.value.trim().length > 0) {
            console.log('Text submitted:', textArea.value);
            // Example: const formData = new FormData(); formData.append('text', textArea.value);
        } else {
            alert('Please select a file or type some text.');
        }

        // Add a visual confirmation for the user
        // alert('Form submitted successfully!');
    });
});