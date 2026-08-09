const BASE_URL = import.meta.env.VITE_API_URL || '/api';

/**
 * Sends a user message to the diagnostic backend and returns the assistant's reply.
 * Expects the backend to expose POST {BASE_URL}/chat accepting { message, history }
 * and returning { reply }. Adjust the shape here if your backend differs.
 *
 * @param {string} message - the user's latest message
 * @param {Array<{role: 'user'|'assistant', content: string}>} history - prior turns
 * @returns {Promise<string>} the assistant's reply text
 */
export async function sendMessage(message, history = []) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history }),
  });

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(
      `Diagnostic service responded with ${response.status}${text ? `: ${text}` : ''}`
    );
  }

  const data = await response.json();

  if (!data || typeof data.reply !== 'string') {
    throw new Error('Diagnostic service returned an unexpected response shape.');
  }

  return data.reply;
}