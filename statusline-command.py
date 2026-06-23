#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json, sys, os, subprocess

data = json.load(sys.stdin)

# Parse fields
model = (data.get('model', {}).get('display_name', 'Claude') or 'Claude').replace('Claude ', '')
cwd = data.get('workspace', {}).get('current_dir', '.') or '.'
cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)
duration_ms = int(data.get('cost', {}).get('total_duration_ms', 0) or 0)
ctx_size = int(data.get('context_window', {}).get('context_window_size', 0) or 0)
lines_add = int(data.get('cost', {}).get('total_lines_added', 0) or 0)
lines_del = int(data.get('cost', {}).get('total_lines_removed', 0) or 0)
rl_pct_raw = data.get('rate_limits', {}).get('five_hour', {}).get('used_percentage', None)

# Tokyo Night colors
PURPLE = '\033[38;5;141m'
GREEN  = '\033[38;5;114m'
CYAN   = '\033[38;5;81m'
DGREEN = '\033[38;5;76m'
RED    = '\033[38;5;203m'
GRAY   = '\033[38;5;245m'
DGRAY  = '\033[38;5;237m'
YELLOW = '\033[38;5;220m'
BOLD   = '\033[1m'
RESET  = '\033[0m'

# Progress bar builder
def make_bar(color, pct_val, width):
    filled = pct_val * width // 100
    empty = width - filled
    return f"{color}{'█' * filled}{DGRAY}{'░' * empty}{RESET}"

# Context bar
ctx_color = RED if pct >= 80 else YELLOW if pct >= 60 else GREEN
ctx_bar = make_bar(ctx_color, pct, 15)
ctx_label = '1M' if ctx_size >= 1000000 else '200k'

# Duration
mins = duration_ms // 60000
secs = (duration_ms % 60000) // 1000

# Session lines
lines_str = ''
if lines_add > 0 or lines_del > 0:
    lines_str = f'  {DGREEN}+{lines_add}{RESET}/{RED}-{lines_del}{RESET}'

# Git branch + dirty count
branch_str = ''
diff_str = ''
try:
    branch = subprocess.check_output(
        ['git', '-C', cwd, 'branch', '--show-current'],
        text=True, stderr=subprocess.DEVNULL
    ).strip()
    if branch:
        branch_str = f'{GREEN}{branch}{RESET}'
    dirty = subprocess.check_output(
        ['git', '-C', cwd, 'status', '--porcelain'],
        text=True, stderr=subprocess.DEVNULL
    ).strip()
    if dirty:
        count = len(dirty.splitlines())
        diff_str = f' {YELLOW}*{count}{RESET}'
except Exception:
    pass

# Rate limit bar
rl_str = ''
if rl_pct_raw is not None:
    rl_int = int(rl_pct_raw)
    rl_color = RED if rl_int >= 80 else YELLOW if rl_int >= 50 else GREEN
    rl_bar = make_bar(rl_color, rl_int, 10)
    rl_str = f'  {DGRAY}|{RESET} RL {rl_bar} {GRAY}{rl_int}%{RESET}'

# Output
dirname = os.path.basename(cwd)
cost_fmt = f'${cost:.2f}'
dur_fmt = f'{mins}:{secs:02d}'

print(f' {PURPLE}{BOLD}{model}{RESET}  {branch_str}{diff_str}  {CYAN}{dirname}{RESET}{lines_str}    {GRAY}{cost_fmt}{RESET}  {GRAY}{dur_fmt}{RESET}')
print(f' CTX {ctx_bar} {GRAY}{pct}%{RESET} {GRAY}{ctx_label}{RESET}{rl_str}')
