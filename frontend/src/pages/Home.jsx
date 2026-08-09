import ChatBox from '../components/ChatBox.jsx';
import './Home.css';

export default function Home() {
  return (
    <main className="home">
      <div className="home__console">
        <ChatBox />
      </div>
      <p className="home__footnote">
        Diagnostic Assistant reads trouble codes and symptoms — it doesn't replace a
        certified mechanic for repairs.
      </p>
    </main>
  );
}