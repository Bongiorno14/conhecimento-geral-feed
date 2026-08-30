# Conhecimento Geral — feed para Alexa

Esse projetinho só tem um trabalho: publicar, todo dia, uma cápsula de
conhecimento geral (a mesma família de conteúdo do quinto eixo do
`professor-marcelo.html`) num link público que a Alexa consegue ler em voz
alta na sua Rotina da manhã.

Não gera conteúdo com IA sozinho — só roda uma vez por dia e avança pra
próxima cápsula de um banco que a gente aprova manualmente (`content.json`).

## Como os arquivos se encaixam

- `content.json` — o banco de cápsulas (categoria + texto). É aqui que
  entram os lotes novos quando a gente gerar mais conteúdo junto.
- `state.json` — só guarda qual é o índice da próxima cápsula a publicar.
- `build_feed.py` — lê os dois de cima e escreve `docs/feed.json` no
  formato exigido pela Amazon (Flash Briefing Skill API).
- `docs/feed.json` — o arquivo que a Alexa realmente consome. Fica
  publicado via GitHub Pages.
- `.github/workflows/daily-feed.yml` — roda `build_feed.py` automaticamente
  todo dia às 05:00 (horário de Brasília), sem precisar mexer em nada.

## Passo 1 — Criar o repositório no GitHub

1. Crie um repositório novo (pode ser público ou privado — GitHub Pages
   funciona nos dois, mas privado exige plano pago pra Pages; se for usar o
   plano gratuito, deixe público, o conteúdo não tem nada sensível).
2. Suba todos os arquivos desta pasta pra esse repositório (mantendo a
   estrutura de pastas, incluindo `.github/workflows/`).

## Passo 2 — Ativar o GitHub Pages

No repositório: **Settings → Pages → Source** → selecione a branch `main`
e a pasta `/docs`. Depois de salvar, o GitHub te dá uma URL parecida com:

```
https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/
```

O feed em si fica em `.../feed.json` (ex:
`https://SEU-USUARIO.github.io/conhecimento-geral-feed/feed.json`).

Depois de saber a URL de verdade, atualize a constante `REDIRECTION_URL`
no topo do `build_feed.py` com ela (é só o link de "saiba mais" que
aparece no app Alexa, não afeta o áudio).

## Passo 3 — Conferir se a automação diária está ativa

A Action em `.github/workflows/daily-feed.yml` já vem configurada pra
rodar sozinha todo dia. Pra confirmar que está ativa: aba **Actions** do
repositório → deve aparecer o workflow "Atualizar cápsula diária
(Conhecimento Geral)" listado. Dá pra rodar manualmente uma vez ali (botão
"Run workflow") só pra testar antes de configurar a Alexa.

## Passo 4 — Criar a Flash Briefing Skill (uma vez só)

1. Acesse o [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
   com sua conta Amazon.
2. Crie uma skill nova do tipo **Flash Briefing**.
3. Adicione um "feed" apontando pra URL do seu `feed.json` (a do Passo 2).
4. Configure o feed como **Text** (não Audio) — a Alexa vai usar
   text-to-speech pra ler o `mainText`.
5. Publique a skill (pode ser em modo de desenvolvimento/privado, não
   precisa passar por certificação pública, já que é só pra uso pessoal).

## Passo 5 — Colocar na Rotina da manhã

No app Alexa: **Mais → Rotinas** → sua rotina da manhã → adicione uma ação
**Flash Briefing** e selecione a skill criada no Passo 4 (ela toca junto
com as outras notícias/briefings que você já tiver configurado).

## Manutenção

Quando a gente gerar um lote novo de cápsulas juntos, é só:

1. Adicionar os novos itens em `content.json` (mesmo formato, só
   `categoria` e `texto`).
2. Também colar as mesmas cápsulas no array `CONHECIMENTO_BANCO` dentro do
   `professor-marcelo.html`, pra manter tracker e feed sincronizados.
3. Dar commit/push — a Action já continua rotacionando normalmente a
   partir daí.
