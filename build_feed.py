#!/usr/bin/env python3
"""
Gera o feed.json da Flash Briefing Skill "Conhecimento Geral" a partir do
banco de cápsulas em content.json, rotacionando uma cápsula por dia.

- content.json: banco de cápsulas curado manualmente (fonte de verdade).
- state.json:   só guarda o índice da próxima cápsula a servir.
- docs/feed.json: saída publicada via GitHub Pages, é o que a Alexa consome.

Rodado 1x por dia via GitHub Actions (.github/workflows/daily-feed.yml).
Não gera conteúdo novo sozinho — só avança a fila do que já foi aprovado.
"""
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTENT_PATH = BASE_DIR / "content.json"
STATE_PATH = BASE_DIR / "state.json"
FEED_PATH = BASE_DIR / "docs" / "feed.json"

# Troque pela URL real do seu GitHub Pages depois de criar o repositório.
REDIRECTION_URL = "https://bongiorno14.github.io/conhecimento-geral-feed/"

# Namespace fixo só pra gerar UUIDs estáveis e reproduzíveis por índice de cápsula.
UUID_NAMESPACE = uuid.UUID("6f1b1a1a-0000-4000-8000-000000000000")


def load_json(path, default):
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    content = load_json(CONTENT_PATH, [])
    if not content:
        raise SystemExit("content.json está vazio — adicione ao menos uma cápsula antes de gerar o feed.")

    state = load_json(STATE_PATH, {"index": 0})
    idx = state.get("index", 0) % len(content)
    capsula = content[idx]

    uid = str(uuid.uuid5(UUID_NAMESPACE, f"capsula-{idx}"))
    update_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.0Z")

    feed_item = {
        "uid": uid,
        "updateDate": update_date,
        "titleText": f"Conhecimento Geral — {capsula['categoria']}",
        "mainText": capsula["texto"],
        "redirectionUrl": REDIRECTION_URL,
    }

    save_json(FEED_PATH, [feed_item])

    # avança pra próxima cápsula amanhã (circular)
    state["index"] = (idx + 1) % len(content)
    save_json(STATE_PATH, state)

    print(f"Feed gerado com a cápsula #{idx} ({capsula['categoria']}). Próximo índice: {state['index']}.")


if __name__ == "__main__":
    main()
