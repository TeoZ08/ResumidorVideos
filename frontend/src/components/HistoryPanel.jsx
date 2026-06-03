export default function HistoryPanel({ history, loading, selectedId, onSelect }) {
  return (
    <aside className="history-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Histórico</p>
          <h2>Resumos salvos</h2>
        </div>
        <span className="counter">{history.length}</span>
      </div>

      <div className="history-list">
        {loading ? (
          <p className="muted">Carregando histórico...</p>
        ) : history.length === 0 ? (
          <p className="muted">Nenhum resumo salvo ainda.</p>
        ) : (
          history.map((item) => (
            <button
              className={`history-item ${selectedId === item.video_id ? "active" : ""}`}
              key={item.video_id}
              type="button"
              onClick={() => onSelect(item.video_id)}
            >
              <span>{item.title}</span>
              <small>{item.created_at || item.video_id}</small>
            </button>
          ))
        )}
      </div>
    </aside>
  );
}
