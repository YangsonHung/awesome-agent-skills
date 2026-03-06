#!/usr/bin/env bash
set -euo pipefail

size_kb() {
  local p="$1"
  if [ -d "$p" ]; then
    local out
    out="$(du -sk "$p" 2>/dev/null || true)"
    if [ -n "$out" ]; then
      awk 'NR==1 {print $1+0}' <<<"$out"
    else
      echo 0
    fi
  else
    echo 0
  fi
}

human() {
  local kb="${1:-0}"
  awk -v kb="$kb" 'BEGIN {
    if (kb >= 1048576) printf "%.2f GB", kb/1048576;
    else if (kb >= 1024) printf "%.2f MB", kb/1024;
    else printf "%d KB", kb;
  }'
}

CACHES="$HOME/Library/Caches"
CORESIM="$HOME/Library/Developer/CoreSimulator"

before_caches=$(size_kb "$CACHES")
before_sim=$(size_kb "$CORESIM")

[ -d "$CACHES" ] && find "$CACHES" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null || true
[ -d "$CORESIM" ] && find "$CORESIM" -mindepth 1 -maxdepth 1 -exec rm -rf {} + 2>/dev/null || true

after_caches=$(size_kb "$CACHES")
after_sim=$(size_kb "$CORESIM")

before_total=$((before_caches + before_sim))
after_total=$((after_caches + after_sim))
freed=$((before_total - after_total))

echo "Caches: $(human "$before_caches") -> $(human "$after_caches")"
echo "CoreSimulator: $(human "$before_sim") -> $(human "$after_sim")"
echo "Total: $(human "$before_total") -> $(human "$after_total")"
echo "Freed: $(human "$freed")"
