import './Message.css';

function formatTimestamp(date) {
  return date.toLocaleTimeString('en-US', {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
}

export default function Message({ role, content, timestamp, isError }) {
  const isUser = role === 'user';

  return (
    <div className={`message message--${isUser ? 'user' : 'bot'}`}>
      {!isUser && <span className="message__icon" aria-hidden="true">🤖</span>}

      <div className={`message__bubble ${isError ? 'message__bubble--error' : ''}`}>
        <p className="message__text">{content}</p>
        <span className="message__meta">
          {isError ? 'ERR' : isUser ? 'YOU' : 'ASSIST'} · {formatTimestamp(timestamp)}
        </span>
      </div>

      {isUser && <span className="message__icon" aria-hidden="true">👤</span>}
    </div>
  );
}