# Case Study — ResumidorVideos

## Problema

Vídeos longos de estudo ou referência exigem tempo para assistir, revisar e transformar em anotações úteis.

## Público-alvo

Estudantes, devs e pessoas que usam vídeos como fonte de estudo e querem transformar conteúdo em resumo reaproveitável.

## Solução

Ferramenta IA que recebe uma URL do YouTube, tenta obter a legenda, envia o texto ao Gemini, salva o resultado em SQLite e permite consultar ou exportar o resumo em Markdown.

## Minha contribuição

A confirmar no detalhe. Pelo código, o projeto inclui CLI, backend FastAPI, frontend React/Vite, cache em SQLite, integração com Gemini e exportação Markdown.

## Stack

- Python
- FastAPI
- SQLite
- pytubefix
- google-genai / Gemini
- React
- Vite

## Arquitetura

O backend concentra a chave do Gemini, a extração da transcrição, o cache e os endpoints. O frontend consome a API para gerar resumo, listar histórico e baixar Markdown. A CLI reutiliza os mesmos serviços do backend.

## Funcionalidades principais

- Resumo de vídeo por URL do YouTube.
- Cache local para evitar chamadas repetidas.
- CLI com opção de salvar Markdown.
- API FastAPI com histórico e exportação.
- Interface web em React/Vite.
- Exportação Markdown em formato útil para base de contexto.

## Decisões técnicas

- Manter `GEMINI_API_KEY` apenas no backend.
- Usar SQLite para cache local simples.
- Reaproveitar serviços entre CLI e API.
- Não implementar transcrição real de áudio nesta etapa.

## Desafios

- Dependência de legendas disponíveis no YouTube.
- Limites de cota e disponibilidade da API Gemini.
- Necessidade futura de fallback mais robusto para vídeos sem legenda.

## Resultado atual

Ferramenta funcional com CLI, API, frontend e exportação Markdown. O projeto está pronto para entrar como ferramenta IA no ecossistema, com limitações claras sobre legendas e cota.

## Demonstração

A confirmar.

## Próximos passos

- Adicionar fallback opcional com `yt-dlp` para legendas automáticas.
- Melhorar extração de pontos principais, conceitos e ações no próprio prompt do Gemini.
- Criar integração controlada com `teo-contexto`.
- Avaliar fila/processamento assíncrono para vídeos mais longos.

## Como este projeto entra no portfólio

Projeto de ferramenta IA útil para estudo e produtividade, mostrando integração com LLM, backend, frontend, persistência local e exportação de conhecimento.
