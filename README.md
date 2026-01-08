# 🎥 Resumidor de Vídeos com IA (Gemini)

Este projeto é uma ferramenta de automação em Python que extrai legendas de vídeos do YouTube e utiliza a Inteligência Artificial do Google (Gemini 1.5 Flash) para gerar resumos concisos.

## 🚀 Funcionalidades

- **Extração via API:** Utiliza `youtube-transcript-api` para obter legendas sem baixar o vídeo pesado.
- **Multilinguagem:** Prioriza legendas em Português, mas aceita Inglês como fallback.
- **Resumo Inteligente:** Processa o texto com o modelo Gemini 1.5 Flash.
- **Leve e Rápido:** Não requer `ffmpeg` nem configuração complexa de cookies.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Google Gen AI SDK** (`google-genai`)
- **Youtube Transcript API:** Para extração leve de texto.
- **python-dotenv:** Gerenciamento seguro de chaves.

## 📦 Instalação

1. Clone o repositório.
2. Crie um ambiente virtual (recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Linux/Mac
   ```
