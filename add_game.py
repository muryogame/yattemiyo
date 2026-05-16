#!/usr/bin/env python3
"""
毎日新しいゲームを追加し、index.htmlを更新するスクリプト。
GitHub Actionsまたはcronで実行する。
"""
import os
import json
import datetime
from pathlib import Path

GAME_DIR = Path(__file__).parent
INDEX_FILE = GAME_DIR / "index.html"
GAMES_LOG = GAME_DIR / "games_log.json"

# 新規ゲームのテンプレートリスト（順番に追加される）
SCHEDULED_GAMES = [
    {
        "id": "typing-speed",
        "title": "⌨️ タイピングゲーム",
        "emoji": "⌨️",
        "cat": "casual brain",
        "tag": "カジュアル・タイピング",
        "rating": "★★★★☆",
        "gradient": "linear-gradient(135deg,#6a3093,#a044ff)",
        "badge": "NEW",
        "badge_class": "new",
    },
    {
        "id": "flappy-bird",
        "title": "🐦 フラッピーバード風",
        "emoji": "🐦",
        "cat": "action casual",
        "tag": "アクション・カジュアル",
        "rating": "★★★★★",
        "gradient": "linear-gradient(135deg,#56ab2f,#a8e063)",
        "badge": "人気",
        "badge_class": "hot",
    },
    {
        "id": "whack-a-mole",
        "title": "🔨 もぐら叩き",
        "emoji": "🔨",
        "cat": "action casual",
        "tag": "アクション・カジュアル",
        "rating": "★★★★☆",
        "gradient": "linear-gradient(135deg,#8B4513,#D2691E)",
        "badge": "NEW",
        "badge_class": "new",
    },
    {
        "id": "simon-says",
        "title": "🔴 サイモンゲーム",
        "emoji": "🔴",
        "cat": "brain casual",
        "tag": "脳トレ・記憶",
        "rating": "★★★★☆",
        "gradient": "linear-gradient(135deg,#cc2b5e,#753a88)",
        "badge": "NEW",
        "badge_class": "new",
    },
    {
        "id": "maze",
        "title": "🌀 迷路ゲーム",
        "emoji": "🌀",
        "cat": "puzzle brain",
        "tag": "パズル・脳トレ",
        "rating": "★★★☆☆",
        "gradient": "linear-gradient(135deg,#1a1a2e,#533483)",
        "badge": "NEW",
        "badge_class": "new",
    },
]


def load_log():
    if GAMES_LOG.exists():
        with open(GAMES_LOG) as f:
            return json.load(f)
    return {"added": [], "last_run": None}


def save_log(log):
    with open(GAMES_LOG, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def game_card_html(g):
    return f"""
    <!-- {g['title']} -->
    <a href="{g['id']}/" class="game-card" data-cat="{g['cat']}" data-name="{g['title']}">
      <div class="game-thumb" style="background:{g['gradient']}">
        {g['emoji']}
        <span class="game-badge {g['badge_class']}">{g['badge']}</span>
      </div>
      <div class="game-info">
        <div class="game-title">{g['title']}</div>
        <div class="game-meta">
          <span class="game-tag">{g['tag']}</span>
          <span class="game-rating">{g['rating']}</span>
        </div>
      </div>
    </a>
"""


def update_index(game):
    content = INDEX_FILE.read_text(encoding="utf-8")
    card = game_card_html(game)
    # Insert before closing </div> of games-grid
    marker = "  </div>\n\n  <!-- Ad mid -->"
    content = content.replace(marker, card + marker, 1)
    INDEX_FILE.write_text(content, encoding="utf-8")
    print(f"index.html updated with: {game['title']}")


def create_game_file(game):
    game_path = GAME_DIR / game["id"]
    game_path.mkdir(exist_ok=True)
    html_file = game_path / "index.html"
    if html_file.exists():
        print(f"Game {game['id']} already exists, skipping file creation")
        return

    # Generic template - to be customized per game
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{game['title']} - ゲームランド</title>
  <style>
    body {{ background:#1a1a2e; color:#e0e0e0; font-family:'Segoe UI',sans-serif; display:flex; flex-direction:column; min-height:100vh; }}
    .top-bar {{ background:#16213e; padding:12px 20px; display:flex; align-items:center; gap:16px; border-bottom:2px solid #6c63ff; }}
    .top-bar a {{ color:#6c63ff; text-decoration:none; }}
    main {{ flex:1; display:flex; align-items:center; justify-content:center; }}
    h1 {{ font-size:2rem; }}
  </style>
</head>
<body>
<div class="top-bar"><a href="../">← ゲーム一覧</a><h1>{game['title']}</h1></div>
<main><h1>🚧 準備中...</h1></main>
</body>
</html>"""
    html_file.write_text(html_content, encoding="utf-8")
    print(f"Created: {html_file}")


def main():
    log = load_log()
    today = datetime.date.today().isoformat()

    if log.get("last_run") == today:
        print(f"Already ran today ({today}). Skipping.")
        return

    # Find next game to add
    added_ids = set(log["added"])
    next_game = None
    for g in SCHEDULED_GAMES:
        if g["id"] not in added_ids:
            next_game = g
            break

    if not next_game:
        print("All scheduled games have been added!")
        return

    print(f"Adding game: {next_game['title']}")
    create_game_file(next_game)
    update_index(next_game)

    log["added"].append(next_game["id"])
    log["last_run"] = today
    save_log(log)
    print(f"Done! Added {next_game['title']}")


if __name__ == "__main__":
    main()
