#!/usr/bin/env bash
# 一鍵安裝 Claude Code 雙行 status line。
# 做兩件事:
#   1. 把 statusline-command.py 複製到 ~/.claude/
#   2. 把 statusLine 設定 merge 進 ~/.claude/settings.json (不動其他設定)
set -euo pipefail

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
SETTINGS="$CLAUDE_DIR/settings.json"

echo "==> 安裝目標: $CLAUDE_DIR"
mkdir -p "$CLAUDE_DIR"

# 1. 複製腳本
cp "$SRC_DIR/statusline-command.py" "$CLAUDE_DIR/statusline-command.py"
chmod +x "$CLAUDE_DIR/statusline-command.py"
echo "[ok] 已複製 statusline-command.py"

# 2. 確認有 python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "[fail] 找不到 python3。Mac 請先裝: xcode-select --install  或  brew install python"
  exit 1
fi

# 3. 安全 merge settings.json 裡的 statusLine 鍵 (保留其他既有設定)
python3 - "$SETTINGS" <<'PY'
import json, os, sys

path = sys.argv[1]
if os.path.exists(path):
    with open(path, encoding="utf-8") as f:
        try:
            cfg = json.load(f)
        except json.JSONDecodeError:
            print("[fail] 現有 settings.json 不是合法 JSON,請先手動處理")
            sys.exit(1)
else:
    cfg = {}

cfg["statusLine"] = {
    "type": "command",
    # 用 $HOME 確保 Mac/Linux 都能正確展開家目錄
    "command": "python3 $HOME/.claude/statusline-command.py",
}

with open(path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, ensure_ascii=False, indent=2)
print("[ok] 已寫入 statusLine 設定 ->", path)
PY

echo
echo "完成。重開一個 Claude Code session 就會看到對話框下面的雙行狀態列。"
