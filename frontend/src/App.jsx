import { useEffect, useState } from "react";

import ErrorAlert from "./components/ErrorAlert.jsx";
import HistoryPanel from "./components/HistoryPanel.jsx";
import LoadingState from "./components/LoadingState.jsx";
import SummaryResult from "./components/SummaryResult.jsx";
import VideoForm from "./components/VideoForm.jsx";
import { getHistory, getHistoryItem, summarizeVideo } from "./lib/api.js";

export default function App() {
  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadHistory() {
    setHistoryLoading(true);
    try {
      const data = await getHistory();
      setHistory(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setHistoryLoading(false);
    }
  }

  useEffect(() => {
    loadHistory();
  }, []);

  async function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const url = String(formData.get("url") || "").trim();
    const force = formData.get("force") === "on";

    if (!url) {
      setError("Informe uma URL válida do YouTube.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await summarizeVideo({ url, force });
      setSummary(data);
      await loadHistory();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleSelectHistory(videoId) {
    setError("");
    try {
      const data = await getHistoryItem(videoId);
      setSummary({ ...data, from_cache: true });
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="app-shell">
      <section className="top-section">
        <div className="brand-block">
          <div className="brand-mark">RV</div>
          <div>
            <h1>Resumidor de Vídeos</h1>
            <p>Cole um link do YouTube e gere um resumo estruturado com IA.</p>
          </div>
        </div>
      </section>

      <section className="workspace">
        <div className="main-column">
          <div className="input-card">
            <VideoForm onSubmit={handleSubmit} loading={loading} />
            <LoadingState active={loading} />
            <ErrorAlert message={error} onClose={() => setError("")} />
          </div>

          <SummaryResult summary={summary} />
        </div>

        <HistoryPanel
          history={history}
          loading={historyLoading}
          selectedId={summary?.video_id}
          onSelect={handleSelectHistory}
        />
      </section>
    </main>
  );
}
