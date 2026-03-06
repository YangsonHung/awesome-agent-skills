#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-$HOME/Library/Application Support}"
LIMIT="${2:-30}"

if [ ! -d "$TARGET" ]; then
  echo "目录不存在: $TARGET"
  exit 1
fi

echo "Priority 2 候选目录（默认只读，不删除）"
echo "扫描目录: $TARGET"
echo "Top $LIMIT"
echo

# 仅输出一级子目录，避免误伤；排序后便于人工确认
find "$TARGET" -mindepth 1 -maxdepth 1 -print0 |
  while IFS= read -r -d '' p; do
    out="$(du -sk "$p" 2>/dev/null || true)"
    if [ -n "$out" ]; then
      awk -F'\t' 'NR==1 {print $1"\t"$2}' <<<"$out"
    fi
  done |
  sort -nr |
  awk -F'\t' -v limit="$LIMIT" '
  function human(kb){
    if (kb >= 1048576) return sprintf("%.2f GB", kb/1048576)
    if (kb >= 1024) return sprintf("%.2f MB", kb/1024)
    return sprintf("%d KB", kb)
  }
  NR <= limit { printf "%s\t%s\n", human($1), $2 }
  '

echo
echo "提示: 优先级2目录通常包含应用业务数据，删除前需逐项确认。"
