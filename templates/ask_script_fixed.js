// Configure marked.js for proper markdown rendering
marked.setOptions({
    highlight: function (code, lang) {
        if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
    },
    breaks: true,
    gfm: true
});

class ChatApp {
    constructor() {
        // Element references
        this.chatMessages = document.getElementById('chatMessages');
        this.chatForm = document.getElementById('chatForm');
        this.askInput = document.getElementById('askInput');
        this.modelSelector = document.getElementById('askModelSelector');
        this.newChatBtn = document.getElementById('newChatBtn');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.sidebarOpenBtn = document.getElementById('sidebarOpenBtn');
        this.chatSidebar = document.getElementById('chatSidebar');
        this.conversationsList = document.getElementById('conversationsList');

        // State
        this.currentConversationId = null;
        this.messageCount = 0;
        this.isLoggedIn = {{ 'true' if user else 'false' }
    };
        this.selectedLanguage = null; // language code (english, telugu, etc.)

// UI translation dictionary
this.translations = {
    english: {
        welcomeTitle: 'JNTU EduAssist AI',
        welcomeMsg: 'Ask me anything about your courses, subjects, or academic topics!',
        tip: "💡 Tip: I'll ask about your preferred language on the first message",
        placeholder: 'Type your question here...',
        sendBtn: 'Send',
        modelLabel: 'Model:'
    },
    telugu: {
        welcomeTitle: 'జంటు ఎడ్యుఎసిస్టెంట్ AI',
        welcomeMsg: 'మీ కోర్సులు, విషయాలు, లేదా అకాడమిక్ టాపిక్స్ గురించి ఏమైనా అడగండి!',
        tip: "💡 సూచన: మొదటి సందేశంలో మీ ఇష్టమైన భాషను అడుగుతాను",
        placeholder: 'మీ ప్రశ్నను ఇక్కడ టైప్ చేయండి...',
        sendBtn: 'పంపండి',
        modelLabel: 'మోడల్:'
    },
    tenglish: {
        welcomeTitle: 'JNTU EduAssist AI',
        welcomeMsg: 'Ask me anything about your courses, subjects, or academic topics!',
        tip: "💡 Tip: I'll ask about your preferred language on the first message",
        placeholder: 'Type your question here...',
        sendBtn: 'Send',
        modelLabel: 'Model:'
    },
    hindi: {
        welcomeTitle: 'JNTU EduAssist AI',
        welcomeMsg: 'अपने कोर्स, विषयों या शैक्षणिक विषयों के बारे में कुछ भी पूछें!',
        tip: "💡 टिप: मैं पहले संदेश में आपकी पसंदीदा भाषा पूछूँगा",
        placeholder: 'अपना प्रश्न यहाँ टाइप करें...',
        sendBtn: 'भेजें',
        modelLabel: 'मॉडल:'
    },
    hinglish: {
        welcomeTitle: 'JNTU EduAssist AI',
        welcomeMsg: 'Apne courses, subjects ya academic topics ke baare mein kuch bhi poochho!',
        tip: "💡 Tip: Main pehle message mein aapki preferred language poochunga",
        placeholder: 'Apna question yahan type karo...',
        sendBtn: 'Send',
        modelLabel: 'Model:'
    },
    arabic: {
        welcomeTitle: 'JNTU EduAssist AI',
        welcomeMsg: 'اسألني أي شيء عن مقرراتك أو مواضيعك الأكاديمية!',
        tip: "💡 ملاحظة: سأطلب منك اختيار اللغة في الرسالة الأولى",
        placeholder: 'اكتب سؤالك هنا...',
        sendBtn: 'إرسال',
        modelLabel: 'النموذج:'
    },
    spanish: {
        welcomeTitle: 'JNTU EduAssist AI',
        welcomeMsg: '¡Pregúntame cualquier cosa sobre tus cursos, materias o temas académicos!',
        tip: "💡 Consejo: Te preguntaré tu idioma preferido en el primer mensaje",
        placeholder: 'Escribe tu pregunta aquí...',
        sendBtn: 'Enviar',
        modelLabel: 'Modelo:'
    },
    french: {
        welcomeTitle: 'JNTU EduAssist AI',
        welcomeMsg: 'Demandez-moi tout sur vos cours, sujets ou sujets académiques!',
        tip: "💡 Astuce : Je vous demanderai votre langue préférée dans le premier message",
        placeholder: 'Tapez votre question ici...',
        sendBtn: 'Envoyer',
        modelLabel: 'Modèle:'
    }
};

this.init();
    }

// Apply UI strings based on selected language (fallback to English)
applyTranslations() {
    const lang = this.selectedLanguage || 'english';
    const t = this.translations[lang] || this.translations['english'];
    if (this.askInput) this.askInput.placeholder = t.placeholder;
    const sendBtn = document.querySelector('.btn-send');
    if (sendBtn) sendBtn.textContent = t.sendBtn;
    const modelLabel = document.querySelector('label[for="askModelSelector"]');
    if (modelLabel) modelLabel.textContent = t.modelLabel;
}

init() {
    // Set UI texts initially
    this.applyTranslations();

    this.chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.sendMessage();
    });

    if (this.newChatBtn) {
        this.newChatBtn.addEventListener('click', () => this.startNewChat());
    }

    if (this.sidebarToggle) {
        this.sidebarToggle.addEventListener('click', () => this.toggleSidebar());
    }

    if (this.sidebarOpenBtn) {
        this.sidebarOpenBtn.addEventListener('click', () => this.toggleSidebar());
    }

    if (this.isLoggedIn) {
        this.loadConversations();
    }
}

toggleSidebar() {
    this.chatSidebar.classList.toggle('collapsed');
}

    async loadConversations() {
    try {
        const response = await fetch('/api/chat/conversations');
        const data = await response.json();
        if (data.success) {
            this.renderConversations(data.conversations);
        }
    } catch (error) {
        console.error('Failed to load conversations:', error);
    }
}

renderConversations(conversations) {
    if (!this.conversationsList) return;
    this.conversationsList.innerHTML = '';
    conversations.forEach(conv => {
        const item = document.createElement('div');
        item.className = 'conversation-item';
        if (conv.id === this.currentConversationId) {
            item.classList.add('active');
        }
        item.innerHTML = `
                <span class="conversation-title">${this.escapeHtml(conv.title)}</span>
                <button class="conversation-delete" data-id="${conv.id}">×</button>
            `;
        item.addEventListener('click', (e) => {
            if (!e.target.classList.contains('conversation-delete')) {
                this.loadConversation(conv.id);
            }
        });
        const deleteBtn = item.querySelector('.conversation-delete');
        deleteBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.deleteConversation(conv.id);
        });
        this.conversationsList.appendChild(item);
    });
}

    async loadConversation(conversationId) {
    try {
        const response = await fetch(`/api/chat/conversation/${conversationId}`);
        const data = await response.json();
        if (data.success) {
            this.currentConversationId = conversationId;
            this.selectedLanguage = data.conversation.language;
            this.chatMessages.innerHTML = '';
            data.conversation.messages.forEach(msg => {
                this.addMessageToUI(msg.content, msg.role);
            });
            this.messageCount = data.conversation.messages.length;
            this.applyTranslations();
            this.loadConversations();
        }
    } catch (error) {
        console.error('Failed to load conversation:', error);
    }
}

    async deleteConversation(conversationId) {
    if (!confirm('Delete this conversation?')) return;
    try {
        const response = await fetch(`/api/chat/conversation/${conversationId}`, { method: 'DELETE' });
        const data = await response.json();
        if (data.success) {
            if (this.currentConversationId === conversationId) {
                this.startNewChat();
            }
            this.loadConversations();
        }
    } catch (error) {
        console.error('Failed to delete conversation:', error);
    }
}

startNewChat() {
    this.currentConversationId = null;
    this.messageCount = 0;
    this.selectedLanguage = null;
    const t = this.translations['english'];
    this.chatMessages.innerHTML = `
            <div class="welcome-message">
                <h2>${t.welcomeTitle}</h2>
                <p>${t.welcomeMsg}</p>
                <p class="welcome-note">${t.tip}</p>
            </div>
        `;
    this.applyTranslations();
    this.loadConversations();
}

    async sendMessage() {
    const message = this.askInput.value.trim();
    if (!message) return;
    const selectedModel = this.modelSelector.value;
    this.addMessageToUI(message, 'user');
    this.askInput.value = '';
    this.askInput.disabled = true;
    const typingId = this.showTyping();
    try {
        if (this.isLoggedIn && !this.currentConversationId) {
            await this.createConversation(message, selectedModel);
        }
        let language = this.selectedLanguage || 'english';
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                model: selectedModel,
                language: language,
                conversation_id: this.currentConversationId
            })
        });
        const data = await response.json();
        this.removeTyping(typingId);
        if (data.success) {
            this.addMessageToUI(data.response, 'assistant', data.model);
            this.messageCount++;
            if (this.messageCount === 1 && !this.selectedLanguage) {
                setTimeout(() => { this.askForLanguage(); }, 500);
            }
        } else {
            this.showError(data.error || 'Failed to get response');
        }
    } catch (error) {
        this.removeTyping(typingId);
        this.showError('Network error. Please try again.');
    } finally {
        this.askInput.disabled = false;
        this.askInput.focus();
    }
}

    async createConversation(firstMessage, model) {
    try {
        const response = await fetch('/api/chat/conversation', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: firstMessage.substring(0, 50) + (firstMessage.length > 50 ? '...' : ''),
                model: model,
                language: this.selectedLanguage || 'english'
            })
        });
        const data = await response.json();
        if (data.success) {
            this.currentConversationId = data.conversation_id;
            this.loadConversations();
        }
    } catch (error) {
        console.error('Failed to create conversation:', error);
    }
}

askForLanguage() {
    const languagePrompt = `
            <div class="message-wrapper message-ai">
                <div class="message-label">System</div>
                <div class="message-content">
                    <p><strong>Which language would you like me to respond in? (English first)</strong></p>
                    <p>Please type one of the following:</p>
                    <ul>
                        <li><strong>English</strong> - For English responses</li>
                        <li><strong>Arabic</strong> - For Arabic responses</li>
                        <li><strong>Spanish</strong> - For Spanish responses</li>
                        <li><strong>French</strong> - For French responses</li>
                        <li><strong>Telugu</strong> - For Telugu responses</li>
                        <li><strong>Tenglish</strong> - For Telugu in English script</li>
                        <li><strong>Hindi</strong> - For Hindi responses</li>
                        <li><strong>Hinglish</strong> - For Hindi in English script</li>
                    </ul>
                    <p><em>I'll remember your choice for this conversation!</em></p>
                </div>
            </div>
        `;
    this.chatMessages.insertAdjacentHTML('beforeend', languagePrompt);
    this.scrollToBottom();
}

addMessageToUI(content, role, modelName = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-wrapper message-${role}`;
    const label = document.createElement('div');
    label.className = 'message-label';
    label.textContent = role === 'user' ? 'You' : (modelName || 'AI');
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    if (role === 'assistant' || role === 'ai') {
        content = content.replace(/\u003cthink\u003e[\\s\\S]*?\u003c\\/think\u003e / gi, '');
        contentDiv.innerHTML = marked.parse(content);
    } else {
        contentDiv.textContent = content;
        const lowerContent = content.toLowerCase();
        if (this.messageCount === 1 && !this.selectedLanguage) {
            if (lowerContent.includes('english')) this.selectedLanguage = 'english';
            else if (lowerContent.includes('arabic')) this.selectedLanguage = 'arabic';
            else if (lowerContent.includes('spanish')) this.selectedLanguage = 'spanish';
            else if (lowerContent.includes('french')) this.selectedLanguage = 'french';
            else if (lowerContent.includes('telugu') && !lowerContent.includes('tenglish')) this.selectedLanguage = 'telugu';
            else if (lowerContent.includes('tenglish')) this.selectedLanguage = 'tenglish';
            else if (lowerContent.includes('hindi') && !lowerContent.includes('hinglish')) this.selectedLanguage = 'hindi';
            else if (lowerContent.includes('hinglish')) this.selectedLanguage = 'hinglish';
            // Apply UI translations once language is detected
            this.applyTranslations();
        }
    }
    messageDiv.appendChild(label);
    messageDiv.appendChild(contentDiv);
    this.chatMessages.appendChild(messageDiv);
    this.scrollToBottom();
}

showTyping() {
    const typingDiv = document.createElement('div');
    const id = 'typing-' + Date.now();
    typingDiv.id = id;
    typingDiv.className = 'message-wrapper message-ai';
    typingDiv.innerHTML = `
            <div class="message-label">AI</div>
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
    this.chatMessages.appendChild(typingDiv);
    this.scrollToBottom();
    return id;
}

removeTyping(id) {
    const typing = document.getElementById(id);
    if (typing) typing.remove();
}

showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'message-wrapper';
    errorDiv.innerHTML = `
            <div class="message-content" style="background: #fef2f2; border-left: 3px solid #ef4444; color: #991b1b;">
                ⚠️ ${this.escapeHtml(message)}
            </div>
        `;
    this.chatMessages.appendChild(errorDiv);
    this.scrollToBottom();
    setTimeout(() => errorDiv.remove(), 5000);
}

scrollToBottom() {
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
}

escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
