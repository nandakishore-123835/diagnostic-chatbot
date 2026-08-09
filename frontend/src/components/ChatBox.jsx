import { useEffect, useRef, useState } from 'react';
import Message from './Message.jsx';
import InputBox from './InputBox.jsx';
import Loading from './Loading.jsx';
import { sendMessage } from '../services/api.js';
import './ChatBox.css';

const GREETING = {
  role: 'assistant',
  content: "Hello! Describe a symptom or paste a trouble code (like P0301) and I'll help diagnose it.",
  timestamp: new Date(),
};

export default function ChatBox() {
  const [messages, setMessages] = useState([GREETING]);
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' });
  }, [messages, isLoading]);

  async function handleSend(text) {
    const userMessage = { role: 'user', content: text, timestamp: new Date() };
    const nextMessages = [...messages, userMessage];
    setMessages(nextMessages);
    setIsLoading(true);

    try {
      const history = nextMessages.map(({ role, content }) => ({ role, content }));
      const reply = await sendMessage(text, history);
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: reply, timestamp: new Date() },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content:
            err instanceof Error
              ? `Couldn't reach the diagnostic service: ${err.message}`
              : "Couldn't reach the diagnostic service. Try again in a moment.",
          timestamp: new Date(),
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="chatbox">
      <header className="chatbox__header">
        <span className="chatbox__title">
          <span aria-hidden="true">🚗</span> Diagnostic Assistant
        </span>
        <span className={`chatbox__status ${isLoading ? 'chatbox__status--active' : ''}`}>
          <span className="chatbox__status-dot" />
          {isLoading ? 'analyzing' : 'online'}
        </span>
      </header>

      <div className="chatbox__messages" ref={scrollRef}>
        {messages.map((m, i) => (
          <Message
            key={i}
            role={m.role}
            content={m.content}
            timestamp={m.timestamp}
            isError={m.isError}
          />
        ))}
        {isLoading && <Loading />}
      </div>

      <InputBox onSend={handleSend} disabled={isLoading} />
    </section>
  );
}