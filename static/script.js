function submitQuery() {
    const chatbox = document.getElementById('chatbox');
    const userQuery = document.getElementById('userQuery').value;
    const fileInput = document.getElementById('pdfUpload');

    // Create user message div and apply class
    const userText = document.createElement('div');
    userText.classList.add('message', 'user');
    userText.innerHTML = userQuery;
    chatbox.appendChild(userText);

    // Add loading message
    const loadingText = document.createElement('div');
    loadingText.id = "loadingMessage";
    loadingText.classList.add('message', 'bot');
    loadingText.innerHTML = `Loading...`;
    chatbox.appendChild(loadingText);
    chatbox.scrollTop = chatbox.scrollHeight;

    // Prepare form data for file and query
    const formData = new FormData();
    formData.append('query', userQuery);

    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);
    }

    // Send request to the Flask backend
    fetch('/query', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Remove loading message
        document.getElementById('loadingMessage').remove();

        // Create bot message div and apply class
        const botText = document.createElement('div');
        botText.classList.add('message', 'bot');
        botText.innerHTML = data.response;
        chatbox.appendChild(botText);
        chatbox.scrollTop = chatbox.scrollHeight;
    });

    // Clear input field
    document.getElementById('userQuery').value = '';
}

function clearChat() {
    document.getElementById('chatbox').innerHTML = '';
}
