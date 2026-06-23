# Claude Code 雙行狀態列 (status line)

在 Claude Code 對話框下面加上一條雙行狀態列:

![status line demo](statusline-demo.png)

第一行: 模型 / git branch(含未提交檔案數) / 目前資料夾 / 本次新增刪除行數 / 花費 / 耗時
第二行: context 使用量進度條 + 5 小時 rate limit 進度條

配色走 Tokyo Night,需要終端機支援 256 色(macOS 內建 Terminal / iTerm2 都可)。

## 安裝 (macOS / Linux)

```bash
git clone <這個 repo 的網址> claude-statusline
cd claude-statusline
bash install.sh
```

裝完重開一個 Claude Code session 就會看到。

`install.sh` 只做兩件事,不會動到你其他設定:
1. 複製 `statusline-command.py` 到 `~/.claude/`
2. 把 `statusLine` 這個鍵 merge 進 `~/.claude/settings.json`

## 前置需求

- 要有 `python3`。Mac 若沒有,跑 `xcode-select --install` 或 `brew install python`。
- 終端機支援 256 色 ANSI(現代終端都有)。

## 手動安裝 (不想跑腳本)

1. 把 `statusline-command.py` 放到 `~/.claude/statusline-command.py`
2. 在 `~/.claude/settings.json` 加上:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 $HOME/.claude/statusline-command.py"
  }
}
```

若 `settings.json` 已有內容,只要把 `statusLine` 這個鍵加進去,不要覆蓋整個檔案。

## 移除

刪掉 `~/.claude/settings.json` 裡的 `statusLine` 區塊即可。
