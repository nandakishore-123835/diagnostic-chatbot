import { useState } from 'react';
import './InputBox.css';

export default function InputBox({ onSend, disabled }) {
  const [value, setValue] = useState('');

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue('');
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  }

  return (
    <form className="input-box" onSubmit={handleSubmit}>
      <textarea
        className="input-box__field"
        placeholder="Describe the symptom or enter a code (e.g. P0301)…"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        rows={1}
        disabled={disabled}
        aria-label="Describe your car problem"
      />
      <button
        type="submit"
        className="input-box__send"
        disabled={disabled || !value.trim()}
        aria-label="Send message"
      >
        ➤
      </button>
    </form>
  );
}