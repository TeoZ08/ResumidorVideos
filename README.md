# 🎥 Resumidor de Vídeos com IA (Gemini)

Este projeto é uma ferramenta de automação em Python que baixa legendas de vídeos do YouTube e utiliza a Inteligência Artificial do Google (Gemini 1.5 Flash) para gerar resumos concisos e estruturados.

## 🚀 Funcionalidades

- **Extração de Legendas:** Baixa automaticamente legendas (PT/EN) de vídeos do YouTube usando `yt-dlp`.
- **Bypass de Bloqueios:** Utiliza `curl_cffi` para simular navegadores reais e evitar erros "429 Too Many Requests" do YouTube.
- **Resumo Inteligente:** Envia o texto da transcrição para a API do Google Gemini para processamento.
- **Modularização:** Código estruturado em módulos independentes para fácil manutenção.

## 🛠️ Tecnologias Utilizadas

- **Python 3.13+**
- **Google Gen AI SDK** (`google-genai`): Nova biblioteca oficial do Google (substituindo a depreciada `google.generativeai`).
- **yt-dlp:** Ferramenta robusta para download de mídia.
- **python-dotenv:** Gerenciamento seguro de chaves de API.

## 📦 Estrutura do Projeto

```text
├── main.py                # Arquivo principal (Maestro). Executa o fluxo completo.
├── audio_transcricao.py   # Módulo responsável por baixar e validar legendas.
├── apigemini.py           # Módulo de conexão com a IA (Client Google).
├── requirements.txt       # Lista de dependências do projeto.
├── .env                   # (Ignorado pelo Git) Armazena a GEMINI_API_KEY.
└── .gitignore             # Configuração para ignorar arquivos temporários e sensíveis.
```
