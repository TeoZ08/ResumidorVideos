export default function VideoForm({ onSubmit, loading }) {
  return (
    <form className="video-form" onSubmit={onSubmit}>
      <label className="field">
        <span>URL do YouTube</span>
        <input
          name="url"
          type="url"
          placeholder="https://www.youtube.com/watch?v=..."
          disabled={loading}
          required
        />
      </label>

      <div className="form-row">
        <label className="switch-line">
          <input name="force" type="checkbox" disabled={loading} />
          <span>Forçar nova análise</span>
        </label>

        <div className="form-actions">
          <button className="secondary-button" type="reset" disabled={loading}>
            Limpar
          </button>
          <button className="primary-button" type="submit" disabled={loading}>
            {loading ? "Processando" : "Gerar resumo"}
          </button>
        </div>
      </div>
    </form>
  );
}
