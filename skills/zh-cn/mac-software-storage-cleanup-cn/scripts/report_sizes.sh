#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-$HOME/software_sizes_report_$(date +%F).txt}"

humanize_kb() {
  awk -F'\t' '
  function human(kb){
    if (kb >= 1048576) return sprintf("%.2f GB", kb/1048576)
    if (kb >= 1024) return sprintf("%.2f MB", kb/1024)
    return sprintf("%d KB", kb)
  }
  { printf "%s\t%s\n", human($1), $2 }
  '
}

collect_dir() {
  local dir="$1"
  if [ -d "$dir" ]; then
    find "$dir" -maxdepth 1 -mindepth 1 ! -name '.DS_Store' ! -name '.localized' -print0 |
      while IFS= read -r -d '' p; do
        du -sk "$p" 2>/dev/null | awk -F'\t' '{print $1"\t"$2}'
      done | sort -nr
  fi
}

{
  echo "软件占用大小报告"
  echo "生成时间: $(date '+%Y-%m-%d %H:%M:%S %Z')"
  echo

  echo "=== /Applications ==="
  collect_dir "/Applications" | humanize_kb
  echo

  echo "=== ~/Applications ==="
  collect_dir "$HOME/Applications" | humanize_kb
  echo

  if command -v brew >/dev/null 2>&1; then
    BREW_PREFIX=$(brew --prefix)
    if [ -d "$BREW_PREFIX/Cellar" ]; then
      echo "=== Homebrew Formula (Cellar) ==="
      collect_dir "$BREW_PREFIX/Cellar" | humanize_kb
      echo
    fi

    if [ -d "$BREW_PREFIX/Caskroom" ]; then
      echo "=== Homebrew Cask (Caskroom) ==="
      collect_dir "$BREW_PREFIX/Caskroom" | humanize_kb
      echo
    fi
  fi
} > "$OUT"

echo "$OUT"
