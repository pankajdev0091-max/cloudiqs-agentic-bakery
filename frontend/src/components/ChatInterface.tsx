'use client';

import { useState, useRef, useEffect, useCallback } from 'react';
import { Send, Loader2, Bot, User, Sparkles, RotateCcw } from 'lucide-react';
import { v4 as uuidv4 } from 'uuid';
import { sendMessage } from '@/lib/api';
import { DemoAgent, generateMockResponse } from '@/lib/agents';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  agent: DemoAgent;
}

export default function ChatInterface({ agent }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId] = useState(() => uuidv4());
  const [backendAvailable, setBackendAvailable] = useState<boolean | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping, scrollToBottom]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSend = async (messageText?: string) => {
    const text = messageText || input.trim();
    if (!text || isTyping) return;

    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content: text,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      // Try backend first
      const response = await sendMessage(agent.id, text, sessionId);
      const assistantMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
      setBackendAvailable(true);
    } catch {
      // Fall back to mock responses
      setBackendAvailable(false);
      // Simulate typing delay for realism
      await new Promise((resolve) => setTimeout(resolve, 800 + Math.random() * 1200));

      const mockContent = generateMockResponse(agent.id, text);
      const assistantMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: mockContent,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true,
    });
  };

  return (
    <div className="flex flex-col h-full">
      {/* Connection status banner */}
      {backendAvailable === false && (
        <div className="px-4 py-2 bg-amber-500/10 border-b border-amber-500/20 text-xs text-amber-400 flex items-center gap-2">
          <Sparkles className="w-3 h-3" />
          Demo mode -- Showing simulated responses. Connect backend at localhost:8000 for live agents.
        </div>
      )}

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="w-16 h-16 rounded-2xl bg-slate-800 flex items-center justify-center mb-4">
              <Bot className="w-8 h-8 text-amber-500" />
            </div>
            <h3 className="text-lg font-semibold text-white mb-2">
              Chat with {agent.name}
            </h3>
            <p className="text-sm text-slate-500 max-w-md mb-6">
              {agent.description}
            </p>

            {/* Suggested prompts */}
            <div className="w-full max-w-lg space-y-2">
              <p className="text-xs text-slate-600 uppercase tracking-wider font-medium mb-3">
                Suggested prompts
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {agent.suggestedPrompts.map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => handleSend(prompt)}
                    className="text-left px-4 py-3 rounded-xl bg-slate-900 border border-slate-800 text-sm text-slate-300 hover:border-amber-500/30 hover:bg-slate-800 transition-smooth"
                  >
                    {prompt}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 message-enter ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {message.role === 'assistant' && (
              <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center flex-shrink-0 mt-1">
                <Bot className="w-4 h-4 text-amber-500" />
              </div>
            )}

            <div className={`max-w-[75%] ${message.role === 'user' ? 'order-first' : ''}`}>
              <div
                className={
                  message.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-agent'
                }
              >
                {/* Render markdown-like content */}
                <div className="text-sm leading-relaxed whitespace-pre-wrap">
                  {message.content.split('\n').map((line, i) => {
                    // Bold
                    const boldProcessed = line.replace(
                      /\*\*(.*?)\*\*/g,
                      '<strong>$1</strong>'
                    );
                    // Code blocks
                    const codeProcessed = boldProcessed.replace(
                      /`([^`]+)`/g,
                      '<code class="bg-slate-700/50 px-1.5 py-0.5 rounded text-xs font-mono text-amber-300">$1</code>'
                    );
                    return (
                      <span key={i}>
                        <span dangerouslySetInnerHTML={{ __html: codeProcessed }} />
                        {i < message.content.split('\n').length - 1 && <br />}
                      </span>
                    );
                  })}
                </div>
              </div>
              <p className={`text-[10px] text-slate-600 mt-1 ${
                message.role === 'user' ? 'text-right' : 'text-left'
              }`}>
                {formatTime(message.timestamp)}
              </p>
            </div>

            {message.role === 'user' && (
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center flex-shrink-0 mt-1">
                <User className="w-4 h-4 text-white" />
              </div>
            )}
          </div>
        ))}

        {/* Typing indicator */}
        {isTyping && (
          <div className="flex gap-3 items-start message-enter">
            <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center flex-shrink-0">
              <Bot className="w-4 h-4 text-amber-500" />
            </div>
            <div className="chat-bubble-agent">
              <div className="flex items-center gap-1.5 py-1">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="border-t border-slate-800 bg-slate-900/50 p-4">
        <div className="flex items-center gap-2 max-w-4xl mx-auto">
          {messages.length > 0 && (
            <button
              onClick={handleClearChat}
              className="p-2.5 rounded-xl text-slate-500 hover:text-white hover:bg-slate-800 transition-smooth flex-shrink-0"
              title="Clear chat"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          )}
          <div className="flex-1 relative">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={`Message ${agent.name}...`}
              disabled={isTyping}
              className="w-full px-4 py-3 bg-slate-800 border border-slate-700 rounded-xl text-sm text-white placeholder-slate-500 focus:border-amber-500/50 focus:ring-2 focus:ring-amber-500/20 transition-smooth disabled:opacity-50"
            />
          </div>
          <button
            onClick={() => handleSend()}
            disabled={!input.trim() || isTyping}
            className="p-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 transition-smooth disabled:opacity-30 disabled:cursor-not-allowed flex-shrink-0"
          >
            {isTyping ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
        <p className="text-[10px] text-slate-600 text-center mt-2">
          Powered by AWS AgentCore & Strands Agents
        </p>
      </div>
    </div>
  );
}
