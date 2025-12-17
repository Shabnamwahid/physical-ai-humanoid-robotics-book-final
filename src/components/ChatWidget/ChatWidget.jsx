import React, { useState, useEffect, useRef } from 'react';
import { useColorMode } from '@docusaurus/theme-common';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import './ChatWidget.css';

const ChatWidget = ({ backendUrl = 'http://localhost:8000' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const { colorMode } = useColorMode();
  const isDarkTheme = colorMode === 'dark';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    // Add user message to the chat
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await fetch(`${backendUrl}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputValue,
          conversation_id: conversationId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Update conversation ID if it's the first message
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // Add bot response to the chat
      const botMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: 'bot',
        sources: data.sources,
        confidence: data.confidence,
        timestamp: data.timestamp
      };

      setMessages([...updatedMessages, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        isError: true,
        timestamp: new Date().toISOString()
      };

      setMessages([...updatedMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  const startNewChat = () => {
    setMessages([]);
    setConversationId(null);
    setInputValue('');
  };

  return (
    <div className={`chat-widget ${isDarkTheme ? 'dark' : 'light'}`}>
      {isOpen ? (
        <div className="chat-container">
          <div className="chat-header">
            <div className="chat-header-left">
              <h3>Physical AI Assistant</h3>
              <span className="chat-status">Online</span>
            </div>
            <div className="chat-header-right">
              <button
                className="new-chat-btn"
                onClick={startNewChat}
                title="Start new conversation"
              >
                + New
              </button>
              <button
                className="close-btn"
                onClick={toggleChat}
                title="Close chat"
              >
                ×
              </button>
            </div>
          </div>

          <div className="chat-messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <h4>Hello! I'm your Physical AI & Humanoid Robotics assistant.</h4>
                <p>Ask me anything about the textbook content:</p>
                <ul>
                  <li>Concepts in Physical AI</li>
                  <li>Humanoid robotics fundamentals</li>
                  <li>ROS 2 and simulation</li>
                  <li>NVIDIA Isaac and navigation</li>
                  <li>Vision-Language-Action systems</li>
                </ul>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
                >
                  <div className="message-content">
                    {message.sender === 'bot' && message.confidence !== undefined && (
                      <div className="confidence-score">
                        Confidence: {(message.confidence * 100).toFixed(1)}%
                      </div>
                    )}
                    <div className="message-text">{message.text}</div>
                    {message.sources && message.sources.length > 0 && (
                      <div className="sources">
                        <strong>Sources:</strong>
                        <ul>
                          {message.sources.slice(0, 3).map((source, index) => (
                            <li key={index}>{source}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message bot">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-area">
            <textarea
              ref={inputRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about Physical AI, robotics, or textbook content..."
              disabled={isLoading}
              rows={2}
            />
            <button
              onClick={sendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </div>
        </div>
      ) : (
        <button className="chat-toggle-button" onClick={toggleChat}>
          <span className="chat-icon">🤖</span>
          <span>Ask AI</span>
        </button>
      )}
    </div>
  );
};

export default ChatWidget;