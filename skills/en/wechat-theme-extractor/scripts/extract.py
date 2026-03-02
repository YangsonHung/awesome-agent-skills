#!/usr/bin/env python3
"""
Minimal WeChat article extractor.
Responsibility: fetch HTML, extract js_content and title.
The AI handles style analysis, theme generation, and config injection.
"""
import re
import subprocess
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract.py <wechat-article-url>")
        sys.exit(1)

    url = sys.argv[1]
    print("Fetching WeChat article...")

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    result = subprocess.run(
        ["curl", "-s", "-A", user_agent, url],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 or not result.stdout:
        print("Failed to fetch article")
        sys.exit(1)

    html = result.stdout
    print(f"Fetched successfully ({len(html):,} chars)")

    title_match = re.search(
        r'<h1[^>]*class="[^"]*rich_media_title[^"]*"[^>]*>(.*?)</h1>',
        html,
        re.DOTALL,
    )
    title = re.sub(r"<[^>]+>", "", title_match.group(1)).strip() if title_match else "Untitled"
    print(f"Title: {title}")

    print("Extracting js_content...")
    content_match = re.search(
        r'id="js_content"[^>]*>(.*?)</div>\s*</div>\s*<script',
        html,
        re.DOTALL,
    )

    if not content_match:
        print("js_content not found")
        sys.exit(1)

    content = content_match.group(1)
    print(f"Extracted successfully ({len(content):,} chars)")

    if getattr(sys, "frozen", False):
        skill_dir = Path(sys.executable).parent
    else:
        skill_dir = Path(__file__).parent

    output_file = skill_dir / ".extracted_content.html"
    with output_file.open("w", encoding="utf-8") as file:
        file.write(f"<!-- Title: {title} -->\n")
        file.write(f"<!-- URL: {url} -->\n")
        file.write(content)

    print(f"Saved to: {output_file}")
    print()
    print("Extraction complete. Ready for AI analysis.")


if __name__ == "__main__":
    main()
