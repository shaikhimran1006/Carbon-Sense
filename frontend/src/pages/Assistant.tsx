import React, { useState } from 'react'
import { Layout } from '../components/Layout'
import { carbonAPI } from '../services/api'
import { Send, Bot, User } from 'lucide-react'

interface Message {
  role: 'user' | 'assistant'
  content: string
  recommendations?: any[]
}

export const Assistant: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: "Hi! I'm your CarbonSense AI assistant. Ask me anything about your carbon footprint or how to reduce it!",
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return
    const userMessage: Message = { role: 'user', content: input }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await carbonAPI.chat(input)
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        recommendations: response.data.recommendations,
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error('Chat failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Layout>
      <div className="h-[calc(100vh-4rem)] md:h-[calc(100vh-3rem)] flex flex-col mb-20 md:mb-0">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">AI Climate Assistant</h1>
          <p className="text-gray-600 dark:text-gray-400">Your personal guide to sustainable living</p>
        </div>

        <div className="flex-1 bg-white dark:bg-gray-800 rounded-2xl shadow-sm p-6 overflow-hidden flex flex-col">
          <div className="flex-1 overflow-y-auto space-y-4 mb-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
              >
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    msg.role === 'user'
                      ? 'bg-green-100 dark:bg-green-900/30'
                      : 'bg-blue-100 dark:bg-blue-900/30'
                  }`}
                >
                  {msg.role === 'user' ? (
                    <User size={20} className="text-green-600 dark:text-green-400" />
                  ) : (
                    <Bot size={20} className="text-blue-600 dark:text-blue-400" />
                  )}
                </div>
                <div
                  className={`max-w-[80%] p-4 rounded-2xl ${
                    msg.role === 'user'
                      ? 'bg-green-600 text-white rounded-tr-md'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white rounded-tl-md'
                  }`}
                >
                  <p>{msg.content}</p>
                  {msg.recommendations && msg.recommendations.length > 0 && (
                    <div className="mt-4 space-y-2">
                      {msg.recommendations.map((rec, i) => (
                        <div
                          key={i}
                          className="p-3 rounded-lg bg-white/10 dark:bg-gray-800/50"
                        >
                          <p className="font-medium">{rec.title}</p>
                          <p className="text-sm opacity-90">{rec.impact}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center">
                  <Bot size={20} className="text-blue-600 dark:text-blue-400" />
                </div>
                <div className="p-4 bg-gray-100 dark:bg-gray-700 rounded-2xl rounded-tl-md">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="flex gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="Ask about your carbon footprint..."
              className="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-green-500 focus:border-transparent outline-none"
            />
            <button
              onClick={handleSend}
              disabled={loading}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-xl transition-colors disabled:opacity-50"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </div>
    </Layout>
  )
}
