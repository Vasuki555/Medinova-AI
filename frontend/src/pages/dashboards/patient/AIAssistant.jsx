/**
 * AI Healthcare Assistant Page
 * Chat with MediNova AI for health questions and report analysis
 */

import { useState, useEffect, useRef } from 'react';
import { apiService } from '@/services/api';
import {
  Bot, Send, User, AlertTriangle, Upload, FileText,
  Sparkles, Loader2, X, RefreshCw, Info, ChevronDown
} from 'lucide-react';

const SUGGESTED_QUESTIONS = [
  "What does a high creatinine level mean?",
  "How can I lower my blood pressure naturally?",
  "What are the symptoms of diabetes?",
  "How do I read my CBC blood test report?",
  "What should I eat if I have high cholesterol?",
  "Is my hemoglobin level of 11 g/dL normal?",
];

const DisclaimerBanner = () => (
  <div className="flex items-start gap-2 p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl text-xs text-amber-800 dark:text-amber-300">
    <AlertTriangle className="w-4 h-4 flex-shrink-0 mt-0.5" />
    <p>
      <strong>Medical Disclaimer:</strong> MediNova AI provides general health information only.
      It does NOT diagnose conditions or replace professional medical advice.
      Always consult your doctor for medical decisions.
    </p>
  </div>
);

const MessageBubble = ({ msg }) => {
  const isUser = msg.role === 'user';

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'} animate-fade-in`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
        isUser
          ? 'bg-primary-500 text-white'
          : 'bg-gradient-to-br from-violet-500 to-primary-500 text-white'
      }`}>
        {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
      </div>

      {/* Bubble */}
      <div className={`max-w-[80%] ${isUser ? 'items-end' : 'items-start'} flex flex-col gap-1`}>
        <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
          isUser
            ? 'bg-primary-500 text-white rounded-tr-md'
            : 'bg-white dark:bg-neutral-800 text-neutral-800 dark:text-neutral-100 border border-neutral-200 dark:border-neutral-700 rounded-tl-md shadow-sm'
        }`}>
          {msg.content}
        </div>
        {msg.timestamp && (
          <span className="text-xs text-neutral-400 px-1">
            {new Date(msg.timestamp).toLocaleTimeString('en', { hour: '2-digit', minute: '2-digit' })}
          </span>
        )}
      </div>
    </div>
  );
};

const TypingIndicator = () => (
  <div className="flex gap-3 animate-fade-in">
    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-500 to-primary-500 text-white flex items-center justify-center flex-shrink-0">
      <Bot className="w-4 h-4" />
    </div>
    <div className="bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 px-4 py-3 rounded-2xl rounded-tl-md shadow-sm">
      <div className="flex gap-1.5 items-center h-5">
        {[0, 1, 2].map(i => (
          <div
            key={i}
            className="w-2 h-2 bg-primary-400 rounded-full animate-bounce"
            style={{ animationDelay: `${i * 0.15}s` }}
          />
        ))}
      </div>
    </div>
  </div>
);

const AIAssistant = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiAvailable, setAiAvailable] = useState(null);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [showSuggestions, setShowSuggestions] = useState(true);

  // Report analysis mode
  const [ocrText, setOcrText] = useState('');
  const [analyzeMode, setAnalyzeMode] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const bottomRef = useRef(null);
  const inputRef = useRef(null);
  const fileInputRef = useRef(null);

  // Scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Load history and check AI status on mount
  useEffect(() => {
    const init = async () => {
      try {
        const [statusRes, historyRes] = await Promise.allSettled([
          apiService.get('/ai/status'),
          apiService.get('/ai/chat/history?limit=20'),
        ]);

        if (statusRes.status === 'fulfilled') {
          setAiAvailable(statusRes.value?.available ?? false);
        }

        if (historyRes.status === 'fulfilled' && historyRes.value?.history?.length > 0) {
          const history = historyRes.value.history;
          const msgs = [];
          history.forEach(turn => {
            if (turn.user_message) msgs.push({ role: 'user', content: turn.user_message, timestamp: turn.timestamp });
            if (turn.assistant_response) msgs.push({ role: 'assistant', content: turn.assistant_response, timestamp: turn.timestamp });
          });
          setMessages(msgs);
          setShowSuggestions(false);
        }
      } catch (err) {
        console.error('AI init error:', err);
      } finally {
        setHistoryLoading(false);
      }
    };
    init();
  }, []);

  const sendMessage = async (text) => {
    const messageText = (text || input).trim();
    if (!messageText || loading) return;

    setInput('');
    setShowSuggestions(false);

    const userMsg = { role: 'user', content: messageText, timestamp: new Date().toISOString() };
    const updatedMessages = [...messages, userMsg];
    setMessages(updatedMessages);
    setLoading(true);

    try {
      // Build history for context (last 10 turns)
      const history = updatedMessages.slice(-10).map(m => ({
        role: m.role === 'user' ? 'user' : 'assistant',
        content: m.content,
      }));

      const res = await apiService.ai('/ai/chat', {
        message: messageText,
        history: history.slice(0, -1), // exclude the current message
      });

      const assistantMsg = {
        role: 'assistant',
        content: res.response || res.error || 'Sorry, I could not process your request.',
        timestamp: res.timestamp || new Date().toISOString(),
      };
      setMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '⚠️ Sorry, I encountered an error. Please check if the AI service is configured. Make sure GEMINI_API_KEY is set in your backend .env file.\n\n⚠️ This is AI-generated information and is not a substitute for professional medical advice.',
        timestamp: new Date().toISOString(),
      }]);
    } finally {
      setLoading(false);
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file size (50MB limit)
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
      alert('File too large. Maximum size is 50MB.');
      if (fileInputRef.current) fileInputRef.current.value = '';
      return;
    }

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/webp', 'application/pdf'];
    if (!allowedTypes.includes(file.type)) {
      alert('Unsupported file type. Please upload JPEG, PNG, WEBP, or PDF files.');
      if (fileInputRef.current) fileInputRef.current.value = '';
      return;
    }

    setUploadLoading(true);
    setUploadProgress(0);

    try {
      // Step 1: Upload and OCR
      const formData = new FormData();
      formData.append('file', file);

      console.log('Uploading file:', file.name, 'Type:', file.type, 'Size:', file.size);

      const ocrRes = await apiService.upload(
        '/ocr/extract',
        formData,
        (progress) => {
          console.log('Upload progress:', progress);
          setUploadProgress(progress);
        }
      );

      console.log('OCR Response:', ocrRes);

      if (!ocrRes.success || !ocrRes.extracted_text) {
        alert('OCR failed: ' + (ocrRes.error || 'Could not extract text from the file. Try a clearer image.'));
        return;
      }

      const extractedText = ocrRes.extracted_text;
      setOcrText(extractedText);

      // Step 2: Analyze with AI
      setMessages(prev => [...prev,
        {
          role: 'user',
          content: `📎 I've uploaded a medical report: "${file.name}". Please analyze it for me.`,
          timestamp: new Date().toISOString(),
        }
      ]);
      setLoading(true);
      setShowSuggestions(false);

      const analysisRes = await apiService.ai('/ai/analyze-report', {
        ocr_text: extractedText,
        report_type: file.type.includes('pdf') ? 'pdf_report' : 'image_report',
      });

      const analysisMsg = {
        role: 'assistant',
        content: analysisRes.analysis || analysisRes.error || 'Could not analyze the report.',
        timestamp: analysisRes.analyzed_at || new Date().toISOString(),
      };
      setMessages(prev => [...prev, analysisMsg]);
    } catch (err) {
      console.error('Upload error:', err);
      const errorDetail = err.response?.data?.detail || err.response?.data?.error || err.message || 'Unknown error';
      alert(`Upload failed: ${errorDetail}\n\nPlease make sure:\n1. File is under 50MB\n2. File is a clear image (PNG/JPG)\n3. Backend server is running`);
    } finally {
      setUploadLoading(false);
      setUploadProgress(0);
      setLoading(false);
      // Reset file input
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  const clearChat = () => {
    setMessages([]);
    setShowSuggestions(true);
    setOcrText('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (historyLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="w-8 h-8 text-primary-500 animate-spin" />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] max-h-[800px] animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-violet-500 to-primary-500 flex items-center justify-center shadow-lg shadow-primary-500/20">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-neutral-900 dark:text-white flex items-center gap-2">
              MediNova AI Assistant
              <Sparkles className="w-4 h-4 text-amber-400" />
            </h1>
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${aiAvailable ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
              <p className="text-xs text-neutral-500 dark:text-neutral-400">
                {aiAvailable === null ? 'Checking...' : aiAvailable ? 'Gemini AI Active' : 'AI not configured — add GEMINI_API_KEY'}
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="p-2 hover:bg-neutral-100 dark:hover:bg-neutral-700 rounded-xl text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-200 transition-colors"
              title="Clear chat"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Disclaimer */}
      <DisclaimerBanner />

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto mt-4 space-y-4 pr-1 scrollbar-thin">

        {/* Welcome state */}
        {messages.length === 0 && (
          <div className="text-center py-8">
            <div className="w-16 h-16 bg-gradient-to-br from-violet-100 to-primary-100 dark:from-violet-900/30 dark:to-primary-900/30 rounded-3xl flex items-center justify-center mx-auto mb-4">
              <Bot className="w-8 h-8 text-primary-500" />
            </div>
            <h2 className="text-lg font-bold text-neutral-900 dark:text-white mb-2">
              How can I help you today?
            </h2>
            <p className="text-neutral-500 dark:text-neutral-400 text-sm max-w-sm mx-auto">
              Ask me about your health, upload a medical report for analysis, or ask general health questions.
            </p>
          </div>
        )}

        {/* Chat messages */}
        {messages.map((msg, i) => (
          <MessageBubble key={i} msg={msg} />
        ))}

        {/* Typing indicator */}
        {loading && <TypingIndicator />}

        <div ref={bottomRef} />
      </div>

      {/* Suggested Questions */}
      {showSuggestions && messages.length === 0 && (
        <div className="mt-4">
          <p className="text-xs font-medium text-neutral-500 dark:text-neutral-400 mb-2">Suggested Questions</p>
          <div className="flex flex-wrap gap-2">
            {SUGGESTED_QUESTIONS.map((q) => (
              <button
                key={q}
                onClick={() => sendMessage(q)}
                disabled={loading}
                className="text-xs bg-neutral-100 dark:bg-neutral-700 text-neutral-700 dark:text-neutral-300 px-3 py-1.5 rounded-xl hover:bg-primary-50 hover:text-primary-700 dark:hover:bg-primary-900/30 dark:hover:text-primary-300 transition-colors"
              >
                {q}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Upload progress */}
      {uploadLoading && (
        <div className="mt-3 p-3 bg-primary-50 dark:bg-primary-900/20 rounded-xl border border-primary-200 dark:border-primary-800">
          <div className="flex items-center justify-between text-xs text-primary-600 dark:text-primary-400 mb-2">
            <span className="flex items-center gap-2">
              <Loader2 className="w-3 h-3 animate-spin" />
              Uploading and analyzing report...
            </span>
            <span>{uploadProgress}%</span>
          </div>
          <div className="w-full h-1.5 bg-primary-100 dark:bg-primary-900 rounded-full overflow-hidden">
            <div
              className="h-full bg-primary-500 rounded-full transition-all"
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="mt-4 bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 rounded-2xl p-3 shadow-sm">
        <textarea
          ref={inputRef}
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a health question or describe your symptoms..."
          rows={2}
          disabled={loading || uploadLoading}
          className="w-full resize-none bg-transparent text-sm text-neutral-800 dark:text-white placeholder:text-neutral-400 focus:outline-none"
        />
        <div className="flex items-center justify-between mt-2">
          <div className="flex items-center gap-2">
            {/* File upload button */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/jpeg,image/png,image/webp,application/pdf"
              onChange={handleFileUpload}
              className="hidden"
              id="ai-file-upload"
            />
            <label
              htmlFor="ai-file-upload"
              className={`flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-xl border transition-colors cursor-pointer ${
                uploadLoading
                  ? 'border-neutral-200 dark:border-neutral-700 text-neutral-300 cursor-not-allowed'
                  : 'border-neutral-300 dark:border-neutral-600 text-neutral-500 dark:text-neutral-400 hover:border-primary-400 hover:text-primary-500'
              }`}
            >
              <Upload className="w-3.5 h-3.5" />
              Upload Report
            </label>
            <span className="text-xs text-neutral-400">JPEG, PNG, PDF · Max 50MB</span>
          </div>

          <button
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading || uploadLoading}
            className="w-9 h-9 bg-primary-500 hover:bg-primary-600 text-white rounded-xl flex items-center justify-center transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-md shadow-primary-500/20"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Send className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIAssistant;
