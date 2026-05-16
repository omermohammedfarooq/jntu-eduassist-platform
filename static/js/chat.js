/**
 * AI Chat Widget JavaScript - Multi-Model Support
 */

class ChatWidget {
    constructor() {
        this.chatButton = document.getElementById('chat-button');
        this.chatWidget = document.getElementById('chat-widget');
        this.chatClose = document.getElementById('chat-close');
        this.chatMessages = document.getElementById('chat-messages');
        this.chatForm = document.getElementById('chat-form');
        this.chatInput = document.getElementById('chat-input');
        this.sendButton = document.getElementById('chat-send');

        this.init();
    }

    init() {
        // Toggle chat widget
        this.chatButton.addEventListener('click', () => this.toggleChat());
        this.chatClose.addEventListener('click', () => this.closeChat());

        // Handle form submission
        this.chatForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Auto-resize input
        this.chatInput.addEventListener('input', () => {
            this.chatInput.style.height = 'auto';
        });

        // Show welcome message
        this.showWelcome();
    }

    toggleChat() {
        this.chatWidget.classList.toggle('open');
        this.chatButton.classList.toggle('active');

        if (this.chatWidget.classList.contains('open')) {
            this.chatInput.focus();
        }
    }

    closeChat() {
        this.chatWidget.classList.remove('open');
        this.chatButton.classList.remove('active');
    }

    showWelcome() {
        const welcome = document.createElement('div');
        welcome.className = 'welcome-message';
        welcome.innerHTML = `
            <h3>👋 Hi! I'm your Navigation Assistant</h3>
            <p>Ask me about website features, how to use JNTU EduAssist, or where to find things!</p>
            <p style="font-size: 11px; margin-top: 0.5rem; color: var(--text-muted);">
                Choose your AI model above 👆<br>
                For academic questions, visit the <strong>Ask Questions</strong> page!
            </p>
        `;
        this.chatMessages.appendChild(welcome);
    }

    async sendMessage() {
        const message = this.chatInput.value.trim();

        if (!message) return;

        // Get selected model
        const modelSelector = document.getElementById('model-selector');
        const selectedModel = modelSelector ? modelSelector.value : 'gemini';

        // Disable input while processing
        this.chatInput.disabled = true;
        this.sendButton.disabled = true;

        // Add user message to chat
        this.addMessage(message, 'user');

        // Clear input
        this.chatInput.value = '';

        // Show typing indicator
        const typingId = this.showTyping();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    model: selectedModel
                })
            });

            const data = await response.json();

            // Remove typing indicator
            this.removeTyping(typingId);

            if (data.success) {
                // Show AI response with model name
                this.addMessage(data.response, 'ai', data.model);
            } else {
                this.showError(data.error || 'Failed to get response');
            }
        } catch (error) {
            this.removeTyping(typingId);
            this.showError('Network error. Please try again.');
        } finally {
            // Re-enable input
            this.chatInput.disabled = false;
            this.sendButton.disabled = false;
            this.chatInput.focus();
        }
    }

    addMessage(content, type, modelName = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;

        const label = document.createElement('div');
        label.className = 'message-label';
        label.textContent = type === 'user' ? 'You' : (modelName || 'AI Assistant');

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // Render markdown for AI messages
        if (type === 'ai') {
            contentDiv.innerHTML = this.renderMarkdown(content);
        } else {
            contentDiv.textContent = content;
        }

        messageDiv.appendChild(label);
        messageDiv.appendChild(contentDiv);

        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    renderMarkdown(text) {
        // Basic markdown rendering
        let html = text
            // Escape HTML first
            .replace(/</g, '&lt;').replace(/>/g, '&gt;')
            // Bold: **text** or __text__
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            .replace(/__(.+?)__/g, '<strong>$1</strong>')
            // Italic: *text* or _text_
            .replace(/\*(.+?)\*/g, '<em>$1</em>')
            .replace(/_(.+?)_/g, '<em>$1</em>')
            // Code: `code`
            .replace(/`(.+?)`/g, '<code>$1</code>')
            // Line breaks
            .replace(/\n/g, '<br>');

        return html;
    }

    showTyping() {
        const typingDiv = document.createElement('div');
        const id = 'typing-' + Date.now();
        typingDiv.id = id;
        typingDiv.className = 'message message-ai';

        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;

        typingDiv.appendChild(indicator);
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();

        return id;
    }

    removeTyping(id) {
        const typing = document.getElementById(id);
        if (typing) {
            typing.remove();
        }
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = `⚠️ ${message}`;

        this.chatMessages.appendChild(errorDiv);
        this.scrollToBottom();

        // Remove error after 5 seconds
        setTimeout(() => errorDiv.remove(), 5000);
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
}

// Initialize chat widget when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatWidget();
});
