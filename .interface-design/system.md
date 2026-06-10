# Sistema de interface — ResumidorVideos

## Intent

Usuário: estudante, dev ou pesquisador que resume vídeos para estudo.

Tarefa principal: colar uma URL, gerar resumo, consultar histórico e exportar Markdown.

Sensação desejada: ferramenta IA clara, focada e confiável, com cara de workspace de estudo.

## Domain

Vídeo, YouTube, legenda, IA, resumo, histórico, Markdown, estudo, contexto, exportação, cache.

## Color World

- Fundo claro quente para leitura prolongada.
- Vermelho controlado como referência ao vídeo/YouTube e ação principal.
- Verde/teal para foco, carregamento e estados de processamento.
- Cinza escuro para texto principal.
- Cinza claro para bordas e separação de painéis.

## Signature

Workspace com formulário, resultado em Markdown e histórico lateral, conectando geração IA com reutilização posterior.

## Defaults a rejeitar

- Chat genérico de IA; preferir ferramenta objetiva de entrada, resultado e histórico.
- Visual de dashboard pesado; preferir área de trabalho leve.
- Botões chamativos demais; preferir hierarquia clara entre gerar, copiar e baixar.

## Tokens e padrões atuais

- Raio: 8px em cards, inputs e botões.
- Superfícies: cards brancos sobre fundo claro quente.
- Depth: sombra suave em painéis principais.
- Ação principal: vermelho; foco e loading: teal.
- Layout: coluna principal + histórico lateral em desktop.

## Estados interativos

- Input de URL deve ter foco visível.
- Botão principal deve indicar estado desabilitado durante carregamento.
- Histórico precisa indicar item selecionado.
- Alertas de erro devem ficar próximos ao formulário.

## Acessibilidade e responsividade

- Manter contraste entre texto, bordas e fundo.
- Preservar leitura confortável do Markdown.
- Garantir que histórico lateral não comprima o resultado no mobile.
- Evitar linhas longas demais no resumo.

## Limites

Não transformar a ferramenta em chat amplo. O fluxo principal é resumir vídeo e exportar conhecimento.
