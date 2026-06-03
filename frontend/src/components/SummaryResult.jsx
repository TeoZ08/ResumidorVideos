import { useState } from "react";

import { getExportUrl } from "../lib/api.js";

function MarkdownView({ text }) {
  const linhas = text.split("\n");

  return (
    <div className="markdown-body">
      {linhas.map((linha, index) => {
        const conteudo = linha.trim();

        if (!conteudo) {
          return <div className="markdown-space" key={index} />;
        }

        if (conteudo.startsWith("### ")) {
          return <h3 key={index}>{conteudo.slice(4)}</h3>;
        }

        if (conteudo.startsWith("## ")) {
          return <h2 key={index}>{conteudo.slice(3)}</h2>;
        }

        if (conteudo.startsWith("# ")) {
          return <h1 key={index}>{conteudo.slice(2)}</h1>;
        }

        if (conteudo.startsWith("- ") || conteudo.startsWith("* ")) {
          return <p className="bullet-line" key={index}>{conteudo.slice(2)}</p>;
        }

        return <p key={index}>{conteudo}</p>;
      })}
    </div>
  );
}

export default function SummaryResult({ summary }) {
  const [copied, setCopied] = useState(false);

  if (!summary) {
    return (
      <section className="result-card empty-state">
        <p>Aguardando URL</p>
      </section>
    );
  }

  async function handleCopy() {
    await navigator.clipboard.writeText(summary.summary);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1800);
  }

  return (
    <section className="result-card">
      <div className="result-header">
        <div>
          <p className="eyebrow">{summary.from_cache ? "Resumo encontrado no cache" : "Resumo final"}</p>
          <h2>{summary.title}</h2>
        </div>

        <div className="result-actions">
          <button className="secondary-button" type="button" onClick={handleCopy}>
            {copied ? "Copiado" : "Copiar"}
          </button>
          <a className="secondary-button" href={getExportUrl(summary.video_id)}>
            Baixar .md
          </a>
        </div>
      </div>

      <dl className="summary-meta">
        <div>
          <dt>ID</dt>
          <dd>{summary.video_id}</dd>
        </div>
        <div>
          <dt>Processado em</dt>
          <dd>{summary.created_at || "Nao informado"}</dd>
        </div>
        <div>
          <dt>Caracteres</dt>
          <dd>{summary.summary.length.toLocaleString("pt-BR")}</dd>
        </div>
      </dl>

      <MarkdownView text={summary.summary} />
    </section>
  );
}
