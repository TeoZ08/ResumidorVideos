export default function ErrorAlert({ message, onClose }) {
  if (!message) {
    return null;
  }

  return (
    <div className="error-alert" role="alert">
      <span>{message}</span>
      <button type="button" onClick={onClose} aria-label="Fechar erro">
        Fechar
      </button>
    </div>
  );
}
