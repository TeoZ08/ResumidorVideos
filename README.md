# 🎥 Resumidor de Vídeos com IA (Gemini)

## Funcionalidades

1. **Pega a legenda:** Baixa o texto do vídeo (mesmo que seja legenda automática).
2. **Resume com IA:** Envia o texto para o Google Gemini gerar um resumo estruturado.
3. **Salva no PC:** Pode salvar o resumo em um arquivo de texto bonitinho (Markdown).
4. **Memória:** Se você pedir o resumo do mesmo vídeo de novo, ele entrega na hora (sem gastar internet ou cota da IA).

## Pré-requisitos

Antes de começar, você precisa ter instalado no seu computador:

- **Python 3.10 ou superior** ([Baixar aqui](https://www.python.org/downloads/))
- **Git** (Opcional, para clonar o projeto)

## Passo a Passo da Instalação

### 1. Baixe o código

Abra o seu terminal (ou prompt de comando) e rode:

```bash
git clone https://github.com/TeoZ08/ResumidorVideos.git
cd ResumidorVideos

```

_(Ou apenas baixe o arquivo ZIP e extraia na sua pasta)._

### 2. Prepare o ambiente (Importante!)

Criar um Ambiente Virtual para o projeto:

**No Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate

```

**No Windows:**

```bash
python -m venv venv
venv\Scripts\activate

```

_Se aparecer `(venv)` no começo da linha do terminal, deu certo!_

### 3. Instale as ferramentas necessárias

Com o ambiente ativado, rode:

```
pip install -r requirements.txt

```

### 4. Configure sua Chave Secreta (API Key)

O programa precisa de uma chave para falar com o Google Gemini.

1. Acesse o [Google AI Studio](https://aistudio.google.com/app/apikey) e clique em **"Create API Key"**.
2. Copie a chave gerada (começa com `AIza...`).
3. Na pasta do projeto, crie um arquivo novo chamado `.env` (apenas `.env`, sem nome antes).
4. Escreva dentro dele:

```env
GEMINI_API_KEY=Cole_Sua_Chave_Aqui

```

---

## 💻 Como Usar

Sempre que for usar, lembre-se de ativar o ambiente virtual (`source venv/bin/activate` ou Windows equivalent).

### 🔹 Apenas ver o resumo na tela

```
python main.py "COLE_A_URL_DO_VIDEO_AQUI"

```

### 🔹 Salvar o resumo em um arquivo

Isso cria um arquivo `.md` no seu computador para ler depois ou reaproveitar em uma base de contexto.

```
python main.py "URL_DO_VIDEO" --salvar

```

O Markdown salvo segue uma estrutura de contexto:

```markdown
# Resumo de vídeo

## Fonte
URL:
Título:
Data de processamento:

## Resumo

## Pontos principais

## Conceitos importantes

## Tarefas/ações sugeridas

## Possível destino no teo-contexto

## Observações
```

### 🔹 Forçar uma nova análise

Se você acha que o resumo antigo ficou ruim e quer tentar de novo do zero:

```
python main.py "URL_DO_VIDEO" --forcar

```

---

## 🌐 Interface web

O projeto agora também possui uma versão web com **FastAPI** no backend e **React + Vite** no frontend. A API do Gemini e o arquivo `.env` continuam apenas no backend.

### Rodar o backend

```bash
uvicorn backend.app.main:app --reload
```

A API ficará disponível em:

```text
http://localhost:8000
```

Endpoints principais:

- `GET /api/health`
- `POST /api/summarize`
- `GET /api/history`
- `GET /api/history/{video_id}`
- `GET /api/export/{video_id}` para baixar Markdown estruturado para contexto

### Rodar o frontend

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

Se necessário, crie `frontend/.env` com:

```env
VITE_API_BASE_URL=http://localhost:8000
```

O frontend ficará disponível em:

```text
http://localhost:5173
```

### Build de produção

```bash
cd frontend
npm install
npm run build
cd ..
uvicorn backend.app.main:app
```

Depois do build, o FastAPI serve os arquivos de `frontend/dist`.

---

## 🚀 Deploy no Render

O arquivo `render.yaml` já define:

- instalação das dependências Python;
- instalação e build do frontend;
- execução do FastAPI com `uvicorn`;
- variáveis `PYTHON_VERSION`, `NODE_VERSION` e `GEMINI_API_KEY`.

No Render, configure `GEMINI_API_KEY` como variável secreta. Não coloque a chave no código, no README ou em arquivos versionados.

## Segurança / Limitações

- `GEMINI_API_KEY` deve ficar apenas no backend.
- O projeto depende de legendas disponíveis no YouTube.
- A exportação Markdown organiza o resumo, mas ainda não extrai automaticamente tarefas e conceitos em campos separados.
- Fallback com `yt-dlp` para legendas automáticas é um próximo passo, não uma dependência ativa neste momento.
- Teo Capture não está implementado aqui; uma integração futura pode enviar resumos revisados para o `teo-contexto`.

## Próximos passos

- Implementar fallback opcional com `yt-dlp`.
- Melhorar o prompt do Gemini para preencher pontos principais, conceitos e tarefas separadamente.
- Criar integração controlada ResumidorVideos → `teo-contexto`.
- Adicionar testes automatizados para serviços de vídeo, resumo, banco e exportação.

## ❓ Problemas Comuns

- **Erro `ModuleNotFoundError`:** Você provavelmente esqueceu de ativar o ambiente virtual (`venv`).
- **Erro 429 (Resource Exhausted):** A API gratuita tem limites. O programa vai esperar 30 segundos e tentar de novo automaticamente.
- **Erro de Legenda:** Alguns vídeos não possuem legendas ou são restritos pelo YouTube.
