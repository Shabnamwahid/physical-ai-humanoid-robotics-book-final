import React from 'react';
import { createRoot } from 'react-dom/client';
import ChatWidget from '@site/src/components/ChatWidget';

let chatRoot = null;

// Initialize the chat widget when the DOM is ready
function initializeChat() {
  // Create a container for the chat widget if it doesn't exist
  let chatContainer = document.getElementById('ai-chat-root');
  if (!chatContainer) {
    chatContainer = document.createElement('div');
    chatContainer.id = 'ai-chat-root';
    document.body.appendChild(chatContainer);
  }

  // Get the backend URL from the config or use default
  const backendUrl = window.chatConfig?.backendUrl || 'http://localhost:8000';

  // Render the chat widget
  chatRoot = createRoot(chatContainer);
  chatRoot.render(<ChatWidget backendUrl={backendUrl} />);
}

// Wait for the DOM to be fully loaded before initializing
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeChat);
} else {
  // DOM is already ready
  initializeChat();
}

// Also initialize when React hydration is complete
// This ensures compatibility with Docusaurus's hydration process
if (typeof window !== 'undefined') {
  window.addEventListener('load', initializeChat);

  // Handle Docusaurus route changes
  if (window.docusaurus) {
    window.docusaurus.eventListeners = window.docusaurus.eventListeners || [];
    window.docusaurus.eventListeners.push({
      onRouteUpdate: () => {
        // Reinitialize if needed when routes change
        setTimeout(initializeChat, 100);
      }
    });
  }
}