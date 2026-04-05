'use client';

import { useEffect, useMemo, useRef, useState } from 'react';
import type { ChatMessage, Persona } from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || 'Empathy Lab AI';

declare global {
  interface Window {
    webkitSpeechRecognition?: new () => SpeechRecognition;
    SpeechRecognition?: new () => SpeechRecognition;
  }

  interface SpeechRecognition extends EventTarget {
    continuous: boolean;
    interimResults: boolean;
    lang: string;
    onstart: (() => void) | null;
    onresult: ((event: SpeechRecognitionEvent) => void) | null;
    onerror: ((event: SpeechRecognitionErrorEvent) => void) | null;
    onend: (() => void) | null;
    start(): void;
    stop(): void;
  }

  interface SpeechRecognitionEvent {
    results: SpeechRecognitionResultList;
  }

  interface SpeechRecognitionResultList {
    [index: number]: SpeechRecognitionResult;
    length: number;
  }

  interface SpeechRecognitionResult {
    [index: number]: SpeechRecognitionAlternative;
    isFinal: boolean;
    length: number;
  }

  interface SpeechRecognitionAlternative {
    transcript: string;
  }

  interface SpeechRecognitionErrorEvent {
    error: string;
  }
}

const CLIENT_ID_KEY = 'empathy-lab-client-id';

function getClientId(): string {
  const existing = window.localStorage.getItem(CLIENT_ID_KEY);
  if (existing) return existing;
  const fresh = crypto.randomUUID();
  window.localStorage.setItem(CLIENT_ID_KEY, fresh);
  return fresh;
}

function setClientId(clientId: string) {
  if (clientId) window.localStorage.setItem(CLIENT_ID_KEY, clientId);
}

export default function ChatWidget({ personas }: { personas: Persona[] }) {
  const [selectedPersona, setSelectedPersona] = useState<string>(personas[0]?.id || 'andrea_miller');
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: 'assistant',
      content: 'Welcome to Empathy Lab AI. Choose a persona, ask a question, or use the microphone to start.'
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [status, setStatus] = useState('Ready');
  const chatEndRef = useRef<HTMLDivElement | null>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const didInitPersonaRef = useRef(false);

  const activePersona = useMemo(
    () => personas.find((persona) => persona.id === selectedPersona) || personas[0],
    [personas, selectedPersona]
  );

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    const SpeechRecognitionCtor = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognitionCtor) return;

    const recognition = new SpeechRecognitionCtor();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    recognition.onstart = () => {
      setIsListening(true);
      setStatus('Listening...');
    };
    recognition.onresult = (event) => {
      const transcript = event.results[0]?.[0]?.transcript || '';
      setInput((previous) => (previous ? `${previous} ${transcript}`.trim() : transcript));
    };
    recognition.onerror = (event) => {
      setStatus(`Voice error: ${event.error}`);
      setIsListening(false);
    };
    recognition.onend = () => {
      setIsListening(false);
      setStatus('Ready');
    };
    recognitionRef.current = recognition;
  }, []);

  useEffect(() => {
    if (!didInitPersonaRef.current) {
      didInitPersonaRef.current = true;
      return;
    }

    void (async () => {
      try {
        await fetch(`${API_BASE}/api/reset`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ client_id: getClientId(), persona_id: selectedPersona })
        });
      } catch {
        // no-op for local/demo reset failures
      }
    })();

    window.speechSynthesis?.cancel();
    setMessages([
      {
        role: 'assistant',
        content: `Persona switched to ${activePersona?.name || APP_NAME}. Previous transcript has been cleared to keep contexts separate.`
      }
    ]);
    setStatus(`Persona: ${activePersona?.name || 'Selected'}`);
  }, [activePersona?.name, selectedPersona]);

  async function sendMessage(messageText?: string) {
    const text = (messageText ?? input).trim();
    if (!text || isLoading) return;

    const nextMessages: ChatMessage[] = [...messages, { role: 'user', content: text }];
    setMessages(nextMessages);
    setInput('');
    setIsLoading(true);
    setStatus('Thinking...');

    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          persona_id: selectedPersona,
          message: text,
          client_id: getClientId()
        })
      });

      if (!response.ok) {
        let errorMessage = 'Request failed';
        try {
          const errorJson = await response.json();
          errorMessage = errorJson?.detail?.message || errorJson?.detail || errorMessage;
        } catch {
          const errorText = await response.text();
          errorMessage = errorText || errorMessage;
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      if (data.client_id) setClientId(data.client_id);
      const assistantMessage: ChatMessage = { role: 'assistant', content: data.reply };
      setMessages([...nextMessages, assistantMessage]);
      setStatus(data.mode === 'demo' ? 'Demo mode' : 'Live AI response');

      if ('speechSynthesis' in window && data.reply) {
        const utterance = new SpeechSynthesisUtterance(data.reply);
        utterance.rate = 1;
        utterance.pitch = 1;
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(utterance);
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      setMessages([
        ...nextMessages,
        { role: 'assistant', content: `There was a problem contacting the backend. ${message}` }
      ]);
      setStatus('Backend error');
    } finally {
      setIsLoading(false);
    }
  }

  async function resetConversation() {
    try {
      const response = await fetch(`${API_BASE}/api/reset`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ client_id: getClientId(), persona_id: selectedPersona })
      });
      if (response.ok) {
        const data = await response.json();
        if (data.client_id) setClientId(data.client_id);
      }
    } catch {
      // no-op for demo reset
    }

    window.speechSynthesis?.cancel();
    setMessages([
      {
        role: 'assistant',
        content: `Conversation reset. You are now chatting with ${activePersona?.name || APP_NAME}.`
      }
    ]);
    setStatus('Ready');
  }

  function toggleListening() {
    const recognition = recognitionRef.current;
    if (!recognition) {
      setStatus('Browser speech recognition is not supported here.');
      return;
    }

    if (isListening) {
      recognition.stop();
      return;
    }

    recognition.start();
  }

  return (
    <section id="demo" className="demo-shell glass-panel">
      <div className="demo-header">
        <div>
          <p className="eyebrow">Live Chatbot Demo</p>
          <h2>Talk to a research-grounded persona</h2>
          <p className="section-copy">
            Choose a persona, ask a question, and explore psychology education through a polished browser-based chat experience.
          </p>
        </div>
        <div className="demo-actions">
          <button className="ghost-button" onClick={resetConversation} type="button">
            Reset
          </button>
          <button className="ghost-button" onClick={toggleListening} type="button">
            {isListening ? 'Stop Mic' : 'Use Mic'}
          </button>
        </div>
      </div>

      <div className="persona-selector" role="tablist" aria-label="Persona selector">
        {personas.map((persona) => (
          <button
            key={persona.id}
            type="button"
            className={`persona-chip ${persona.id === selectedPersona ? 'active' : ''}`}
            onClick={() => setSelectedPersona(persona.id)}
          >
            <span>{persona.name}</span>
            <small>{persona.title}</small>
          </button>
        ))}
      </div>

      <div className="chat-grid">
        <aside className="persona-card glass-card">
          <span className="accent-dot" style={{ background: activePersona?.accent }} />
          <h3>{activePersona?.name}</h3>
          <p className="persona-title">{activePersona?.title}</p>
          <p>{activePersona?.summary}</p>
          <div className="status-pill">{status}</div>
        </aside>

        <div className="chat-card glass-card">
          <div className="message-list">
            {messages.map((message, index) => (
              <div key={`${message.role}-${index}`} className={`message-row ${message.role}`}>
                <div className="message-bubble">{message.content}</div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          <form
            className="composer"
            onSubmit={(event) => {
              event.preventDefault();
              void sendMessage();
            }}
          >
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask about symptoms, experiences, treatment approaches, or the project itself..."
              rows={3}
            />
            <div className="composer-actions">
              <button type="button" className="ghost-button" onClick={() => window.speechSynthesis?.cancel()}>
                Mute Voice
              </button>
              <button type="submit" className="primary-button" disabled={isLoading}>
                {isLoading ? 'Sending...' : 'Send'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </section>
  );
}
