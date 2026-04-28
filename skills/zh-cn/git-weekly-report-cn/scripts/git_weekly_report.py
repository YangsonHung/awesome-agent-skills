#!/usr/bin/env python3
"""Extract git commit logs as structured JSON for weekly report generation."""

import argparse
import json
import os
import subprocess
import sys
from datetime import date, timedelta

MAX_BODY_LENGTH = 500


def run_git_log(repo_path, since, until, author=None, no_merges=True):
    """Run git log in a repo and return parsed commit entries."""
    cmd = ["git", "-C", repo_path, "log", "--all"]
    if no_merges:
        cmd.append("--no-merges")
    cmd.append(f"--since={since}")
    cmd.append(f"--until={until} 23:59:59")
    if author:
        cmd.append(f"--author={author}")
    # %x00 = NUL (record separator), %x01 = SOH (field separator)
    cmd.append("--format=%H%x01%h%x01%an%x01%aI%x01%s%x01%b%x01%D%x00")

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
    except FileNotFoundError:
        print("Error: git not found on PATH", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        print(f"Warning: git log failed for {repo_path}: {result.stderr.strip()}", file=sys.stderr)
        return []

    commits = []
    for record in result.stdout.split("\x00"):
        record = record.strip()
        if not record:
            continue
        parts = record.split("\x01")
        if len(parts) < 7:
            print(f"Warning: skipping malformed record: {record[:80]}", file=sys.stderr)
            continue
        body = parts[5].strip()
        if len(body) > MAX_BODY_LENGTH:
            body = body[:MAX_BODY_LENGTH] + "..."
        commits.append({
            "hash": parts[0],
            "short_hash": parts[1],
            "author": parts[2],
            "date": parts[3],
            "subject": parts[4],
            "body": body,
            "refs": parts[6],
        })

    return commits


def is_git_repo(path):
    """Check if a path is a git repository."""
    try:
        result = subprocess.run(
            ["git", "-C", path, "rev-parse", "--git-dir"],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Extract git commit logs as structured JSON for weekly reports"
    )
    parser.add_argument(
        "--since",
        default=None,
        help="Start date (YYYY-MM-DD), default: 7 days ago",
    )
    parser.add_argument(
        "--until",
        default=None,
        help="End date (YYYY-MM-DD), default: today",
    )
    parser.add_argument(
        "--author",
        default=None,
        help="Filter commits by author (substring match)",
    )
    parser.add_argument(
        "--repo",
        nargs="+",
        default=None,
        help="One or more git repository paths (default: current directory)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--no-merges",
        action="store_true",
        default=True,
        help="Exclude merge commits (default: True)",
    )
    parser.add_argument(
        "--merges",
        action="store_true",
        default=False,
        help="Include merge commits",
    )

    args = parser.parse_args()

    today = date.today()
    since = args.since or (today - timedelta(days=7)).isoformat()
    until = args.until or today.isoformat()
    no_merges = not args.merges
    repos = args.repo or [os.getcwd()]

    output = {
        "date_range": {"since": since, "until": until},
        "author_filter": args.author,
        "repositories": [],
        "total_commits": 0,
    }

    for repo_path in repos:
        repo_path = os.path.abspath(repo_path)
        if not is_git_repo(repo_path):
            print(f"Warning: {repo_path} is not a git repository, skipping", file=sys.stderr)
            continue

        repo_name = os.path.basename(repo_path)
        commits = run_git_log(repo_path, since, until, args.author, no_merges)

        output["repositories"].append({
            "path": repo_path,
            "name": repo_name,
            "commit_count": len(commits),
            "commits": commits,
        })
        output["total_commits"] += len(commits)

    json_str = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_str)
    else:
        print(json_str)


if __name__ == "__main__":
    main()
