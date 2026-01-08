# 🎥 Resumidor de Vídeos com IA (Gemini)

Uma ferramenta simples e poderosa que assiste a vídeos do YouTube por você!
Este programa baixa as legendas de um vídeo e usa a Inteligência Artificial do Google (Gemini) para criar um resumo com os pontos principais.

Ideal para estudantes e desenvolvedores que querem economizar tempo.

## ✨ O que ele faz?

1. **Pega a legenda:** Baixa o texto do vídeo (mesmo que seja legenda automática).
2. **Resume com IA:** Envia o texto para o Google Gemini gerar um resumo estruturado.
3. **Salva no PC:** Pode salvar o resumo em um arquivo de texto bonitinho (Markdown).
4. **Memória:** Se você pedir o resumo do mesmo vídeo de novo, ele entrega na hora (sem gastar internet ou cota da IA).

## 🛠️ Pré-requisitos

Antes de começar, você precisa ter instalado no seu computador:

- **Python 3.10 ou superior** ([Baixar aqui](https://www.python.org/downloads/))
- **Git** (Opcional, para clonar o projeto)

## 🚀 Passo a Passo da Instalação

### 1. Baixe o código

Abra o seu terminal (ou prompt de comando) e rode:

```bash
git clone [https://github.com/SEU-USUARIO/NOME-DO-REPO.git](https://github.com/SEU-USUARIO/NOME-DO-REPO.git)
cd TranscricaoPython

```

_(Ou apenas baixe o arquivo ZIP e extraia na sua pasta)._

### 2. Prepare o ambiente (Importante!)

Para não bagunçar seu computador, vamos criar uma "caixa" isolada para o projeto (Ambiente Virtual):

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

Isso cria um arquivo `.md` no seu computador para ler depois.

```
python main.py "URL_DO_VIDEO" --salvar

```

### 🔹 Forçar uma nova análise

Se você acha que o resumo antigo ficou ruim e quer tentar de novo do zero:

```
python main.py "URL_DO_VIDEO" --forcar

```

## ❓ Problemas Comuns

- **Erro `ModuleNotFoundError`:** Você provavelmente esqueceu de ativar o ambiente virtual (`venv`).
- **Erro 429 (Resource Exhausted):** A API gratuita tem limites. O programa vai esperar 30 segundos e tentar de novo automaticamente.
- **Erro de Legenda:** Alguns vídeos não possuem legendas ou são restritos pelo YouTube.
