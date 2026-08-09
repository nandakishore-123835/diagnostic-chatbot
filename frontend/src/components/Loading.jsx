import './Loading.css';

export default function Loading() {
  return (
    <div className="loading" role="status" aria-label="Assistant is analyzing">
      <span className="loading__dot" />
      <span className="loading__dot" />
      <span className="loading__dot" />
      <span className="loading__label">reading codes&hellip;</span>
    </div>
  );
}