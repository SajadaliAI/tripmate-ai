// Auto-resize textarea input
const userInput = document.getElementById('userInput');
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});

// Allow 'Enter' key to send (Shift + Enter for new line)
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        handleSend(event);
    }
}

// Quick prompt clicked from chips
function usePrompt(text) {
    userInput.value = text;
    userInput.style.height = 'auto';
    userInput.style.height = (userInput.scrollHeight) + 'px';
    handleSend(new Event('submit'));
}

// Start New Chat Session
function startNewChat() {
    const chatBox = document.getElementById('chatBox');
    const welcomeScreen = document.getElementById('welcomeScreen');
    
    chatBox.innerHTML = '';
    welcomeScreen.style.display = 'flex';
    userInput.value = '';
    userInput.style.height = 'auto';
}

// Handle Form Submission
async function handleSend(event) {
    if (event) event.preventDefault();

    const promptText = userInput.value.trim();
    if (!promptText) return;

    // Hide welcome banner
    const welcomeScreen = document.getElementById('welcomeScreen');
    if (welcomeScreen) {
        welcomeScreen.style.display = 'none';
    }

    // Append User Message
    appendMessage(promptText, 'user');
    
    // Reset Input
    userInput.value = '';
    userInput.style.height = 'auto';

    // Show Loader
    showLoading(true);

    try {
        const response = await fetch('/api/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: promptText })
        });

        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }

        const data = await response.json();
        const botReply = data.response || data.plan || "Trip plan generated successfully!";
        
        appendMessage(botReply, 'bot');

    } catch (error) {
        console.error('Error fetching itinerary:', error);
        appendMessage('⚠️ **Service Notice:** Unable to reach AI agents right now. Please verify your connection or API keys.', 'bot');
    } finally {
        showLoading(false);
    }
}

// Append Message with Markdown Parser (Marked.js)
function appendMessage(text, sender) {
    const chatBox = document.getElementById('chatBox');
    const msgDiv = document.createElement('div');
    
    msgDiv.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    
    // Use Marked.js to convert Markdown to Rich HTML (Tables, Bold, Lists)
    if (typeof marked !== 'undefined' && sender === 'bot') {
        msgDiv.innerHTML = marked.parse(text);
    } else {
        let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        msgDiv.innerHTML = `<p>${formattedText}</p>`;
    }

    chatBox.appendChild(msgDiv);
    
    // Smooth Scroll to view
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Toggle Loading Card
function showLoading(isLoading) {
    const loader = document.getElementById('loadingIndicator');
    const chatBox = document.getElementById('chatBox');
    
    if (isLoading) {
        loader.classList.remove('hidden');
        chatBox.scrollTop = chatBox.scrollHeight;
    } else {
        loader.classList.add('hidden');
    }
}