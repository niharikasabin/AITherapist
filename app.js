// Function to handle sending messages to the Flask backend
function sendMessage() {
    const message = document.getElementById('messageInput').value;  // Get message from input field

    if (message.trim() === "") {
        alert("Please enter a message.");
        return;
    }

    // Display user's message in the chatbox
    const chatbox = document.getElementById('chatbox');
    chatbox.innerHTML += `<div class="message">You: ${message}</div>`;

    // Send message to Flask backend
    fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),  // Send message as JSON
    })
    .then(response => response.json())  // Get response as JSON
    .then(data => {
        // Display AI's response in the chatbox
        chatbox.innerHTML += `<div class="message">Therapist: ${data.response}</div>`;

        // Clear input box and scroll to the bottom of chat
        document.getElementById('messageInput').value = '';
        chatbox.scrollTop = chatbox.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);  // Log any errors in the console
    });
}

// Optional: Allow sending message by pressing Enter key
document.getElementById('messageInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});
