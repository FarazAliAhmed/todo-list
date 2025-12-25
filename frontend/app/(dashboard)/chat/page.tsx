"use client";

import { useState, useRef, useEffect } from "react";
import { useAuth } from "@/hooks/useAuth";
import ProtectedRoute from "@/components/ProtectedRoute";
import { api } from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  toolCalls?: Array<{
    tool_name: string;
    arguments: Record<string, unknown>;
    result: Record<string, unknown>;
  }>;
}

export default function ChatPage() {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | undefined>();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !user?.id) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await api.sendChatMessage(
        user.id,
        userMessage.content,
        conversationId
      );

      setConversationId(response.conversation_id);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.response,
        timestamp: new Date(),
        toolCalls: response.tool_calls,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I encountered an error. Please try again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const startNewConversation = () => {
    setMessages([]);
    setConversationId(undefined);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 flex flex-col">
        <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full p-4">
          {/* Chat header */}
          <div className="bg-white rounded-t-lg shadow-sm border border-b-0 p-4 flex justify-between items-center">
            <div>
              <h1 className="text-xl font-semibold text-gray-900">AI Task Assistant</h1>
              <p className="text-sm text-gray-500">
                Manage your tasks with natural language
              </p>
            </div>
            <button
              onClick={startNewConversation}
              className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              New Chat
            </button>
          </div>

          {/* Messages area */}
          <div className="flex-1 bg-white border-x overflow-y-auto p-4 space-y-4 min-h-[400px] max-h-[60vh]">
            {messages.length === 0 ? (
              <div className="text-center text-gray-500 py-12">
                <div className="w-16 h-16 mx-auto mb-4 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                  </svg>
                </div>
                <h3 className="text-lg font-medium mb-2">Start a conversation</h3>
                <p className="text-sm max-w-md mx-auto">
                  Try saying things like:
                </p>
                <div className="mt-4 space-y-2">
                  <button
                    onClick={() => setInput("Show me all my tasks")}
                    className="block mx-auto px-4 py-2 bg-gray-100 rounded-lg text-sm hover:bg-gray-200 transition-colors"
                  >
                    &quot;Show me all my tasks&quot;
                  </button>
                  <button
                    onClick={() => setInput("Add a task to buy groceries")}
                    className="block mx-auto px-4 py-2 bg-gray-100 rounded-lg text-sm hover:bg-gray-200 transition-colors"
                  >
                    &quot;Add a task to buy groceries&quot;
                  </button>
                  <button
                    onClick={() => setInput("What tasks are pending?")}
                    className="block mx-auto px-4 py-2 bg-gray-100 rounded-lg text-sm hover:bg-gray-200 transition-colors"
                  >
                    &quot;What tasks are pending?&quot;
                  </button>
                </div>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      message.role === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-gray-100 text-gray-900"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>
                    {message.toolCalls && message.toolCalls.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <p className="text-xs text-gray-500 mb-1">Actions taken:</p>
                        {message.toolCalls.map((tc, idx) => (
                          <span
                            key={idx}
                            className="inline-block text-xs bg-gray-200 text-gray-700 px-2 py-1 rounded mr-1 mb-1"
                          >
                            {tc.tool_name}
                          </span>
                        ))}
                      </div>
                    )}
                    <p className={`text-xs mt-2 ${message.role === "user" ? "text-blue-200" : "text-gray-400"}`}>
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-lg p-4">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input area */}
          <form onSubmit={handleSubmit} className="bg-white rounded-b-lg shadow-sm border p-4">
            <div className="flex space-x-4">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message... (e.g., 'Add a task to call mom')"
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                style={{ color: '#000000' }}
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
              >
                <span>Send</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </form>
        </div>
      </div>
    </ProtectedRoute>
  );
}
