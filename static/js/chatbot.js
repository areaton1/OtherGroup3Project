// Chatbot JavaScript (shared across pages)

const chatForm = document.getElementById('chatForm');
const chatInput = document.getElementById('chatInput');
const chatMessages = document.getElementById('chatMessages');

let isProcessing = false;

// Handle chat form submission
chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  if (isProcessing) return;

  const message = chatInput.value.trim();
  if (!message) return;

  // Add user message to chat
  addMessage('user', message);

  // Clear input
  chatInput.value = '';

  // Show loading
  isProcessing = true;
  const loadingId = addLoadingMessage();

  try {
    const response = await fetch('/api/chatbot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    // Remove loading message
    removeMessage(loadingId);

    if (!response.ok) {
      addMessage('ai', `Error: ${data.error || 'Failed to get response'}`);
      return;
    }

    // Add AI response
    addMessage('ai', data.response);

    // Show related CVEs if any
    if (data.related_cves && data.related_cves.length > 0) {
      addRelatedCVEs(data.related_cves);
    }
  } catch (error) {
    console.error('Chat error:', error);
    removeMessage(loadingId);
    addMessage('ai', 'Sorry, I encountered an error. Please try again.');
  } finally {
    isProcessing = false;
  }
});

function addMessage(type, text) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message ${type}`;

  const header = document.createElement('div');
  header.className = 'message-header';
  header.textContent = type === 'user' ? 'You' : 'AI Assistant';

  const content = document.createElement('div');
  content.textContent = text;

  messageDiv.appendChild(header);
  messageDiv.appendChild(content);

  // Remove welcome message if exists
  const welcome = chatMessages.querySelector('.text-center');
  if (welcome) {
    welcome.remove();
  }

  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return messageDiv;
}

function addLoadingMessage() {
  const loadingDiv = document.createElement('div');
  loadingDiv.className = 'chat-message ai';
  loadingDiv.id = 'loading-message';

  const header = document.createElement('div');
  header.className = 'message-header';
  header.textContent = 'AI Assistant';

  const content = document.createElement('div');
  content.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Thinking...';

  loadingDiv.appendChild(header);
  loadingDiv.appendChild(content);

  chatMessages.appendChild(loadingDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;

  return 'loading-message';
}

function removeMessage(id) {
  const message = document.getElementById(id);
  if (message) {
    message.remove();
  }
}

function addRelatedCVEs(cves) {
  const relatedDiv = document.createElement('div');
  relatedDiv.className = 'chat-message ai';

  const header = document.createElement('div');
  header.className = 'message-header';
  header.textContent = 'Related CVEs from Database';

  const content = document.createElement('div');
  content.className = 'small';

  const list = document.createElement('ul');
  list.className = 'mb-0 ps-3';

  cves.forEach((cve) => {
    const li = document.createElement('li');
    li.innerHTML = `
      <strong>${escapeHtml(cve.cve_id)}</strong>: ${escapeHtml(cve.title)}
      <br><small class="text-muted">${escapeHtml(cve.vendor)} - ${escapeHtml(cve.severity)}</small>
    `;
    list.appendChild(li);
  });

  content.appendChild(list);
  relatedDiv.appendChild(header);
  relatedDiv.appendChild(content);

  chatMessages.appendChild(relatedDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
  if (!text) return '';
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

// Clear chat when modal is closed
const chatModal = document.getElementById('chatModal');
if (chatModal) {
  chatModal.addEventListener('hidden.bs.modal', () => {
    // Optionally clear chat history when modal closes
    // Uncomment below to reset chat on close
    // chatMessages.innerHTML = '<div class="text-center text-muted py-5"><span class="fs-1">🤖</span><p class="mt-3">Ask me anything about CVEs and cybersecurity!</p></div>';
  });
}

