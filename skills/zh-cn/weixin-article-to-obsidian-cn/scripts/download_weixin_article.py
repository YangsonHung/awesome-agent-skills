#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import datetime as dt
import html as html_lib
import json
import mimetypes
import os
import re
import shutil
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/126.0.0.0 Safari/537.36"
)


def fetch_bytes(url: str, referer: str | None = None, timeout: int = 30) -> tuple[bytes, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if referer:
        headers["Referer"] = referer
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        content_type = resp.headers.get("Content-Type", "")
        return resp.read(), content_type


def fetch_text(url: str) -> str:
    data, content_type = fetch_bytes(url)
    charset = "utf-8"
    match = re.search(r"charset=([\w-]+)", content_type, re.I)
    if match:
        charset = match.group(1)
    return data.decode(charset, errors="replace")


def decode_js_literal(value: str) -> str:
    try:
        decoded = ast.literal_eval(value)
    except Exception:
        decoded = value.strip("\"'")
    return html_lib.unescape(str(decoded))


def decode_escaped_text(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        if token.startswith("\\x"):
            return chr(int(token[2:], 16))
        if token.startswith("\\u"):
            return chr(int(token[2:], 16))
        return {
            "\\n": "\n",
            "\\r": "\n",
            "\\t": "\t",
            "\\/": "/",
            "\\\\": "\\",
        }.get(token, token[-1])

    text = re.sub(r"\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|\\[nrt/\\]", replace, value)
    return html_lib.unescape(html_lib.unescape(text))


def clean_text(text: str) -> str:
    text = re.sub(r"<\s*(br|p|div|section|li|h[1-6])\b[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"</\s*(p|div|section|li|h[1-6])\s*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_lib.unescape(text)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    kept: list[str] = []
    previous_blank = False
    for line in lines:
        if not line:
            if kept and not previous_blank:
                kept.append("")
            previous_blank = True
            continue
        kept.append(line)
        previous_blank = False
    return "\n".join(kept).strip()


def extract_meta_content(page_html: str, name: str) -> str:
    patterns = [
        rf'<meta\s+name="{re.escape(name)}"\s+content="(.*?)"\s*/?>',
        rf'<meta\s+property="{re.escape(name)}"\s+content="(.*?)"\s*/?>',
    ]
    for pattern in patterns:
        match = re.search(pattern, page_html, re.I | re.S)
        if match:
            return decode_escaped_text(match.group(1)).strip()
    return ""


def extract_js_var(page_html: str, name: str) -> str:
    string_pattern = r"""('(?:\\.|[^'])*'|"(?:\\.|[^"])*")"""
    pattern = rf"(?:var\s+{re.escape(name)}|window\.{re.escape(name)})\s*=\s*{string_pattern}"
    match = re.search(pattern, page_html, re.S)
    return decode_js_literal(match.group(1)).strip() if match else ""


def extract_author(page_html: str) -> str:
    for field in ["author", "og:article:author"]:
        author = extract_meta_content(page_html, field)
        if author:
            return clean_text(author)
    match = re.search(r'class="wx_follow_nickname"[^>]*>(.*?)</div>', page_html, re.I | re.S)
    if match:
        return clean_text(match.group(1))
    for var_name in ["nickname", "user_name"]:
        value = extract_js_var(page_html, var_name)
        if value:
            return value
    return ""


def extract_title(page_html: str) -> str:
    for field in ["og:title", "twitter:title", "title"]:
        title = extract_meta_content(page_html, field)
        if title:
            return clean_text(title)
    value = extract_js_var(page_html, "msg_title")
    return value or "weixin-article"


def extract_publish_time(page_html: str) -> str:
    publish_time = extract_js_var(page_html, "publish_time")
    if publish_time:
        return publish_time
    for var_name in ["ct", "ori_create_time"]:
        raw = extract_js_var(page_html, var_name)
        if raw and raw.isdigit():
            tz = ZoneInfo("Asia/Shanghai") if ZoneInfo else None
            timestamp = int(raw)
            moment = dt.datetime.fromtimestamp(timestamp, tz=tz)
            return moment.strftime("%Y-%m-%d %H:%M")
    return ""


def extract_body_text(page_html: str, opencli_body: str | None) -> str:
    description = extract_meta_content(page_html, "description")
    body_from_description = clean_text(description) if description else ""

    if opencli_body:
        if not body_from_description:
            return opencli_body
        if len(opencli_body) > max(260, int(len(body_from_description) * 1.4)):
            return opencli_body
    return body_from_description or (opencli_body or "")


def extract_picture_urls(page_html: str) -> list[str]:
    urls: list[str] = []
    picture_block = re.search(
        r"window\.picture_page_info_list\s*=\s*\[(.*?)\]\s*;",
        page_html,
        re.S,
    )
    if picture_block:
        block = picture_block.group(1)
        for match in re.finditer(r"cdn_url:\s*('(?:\\.|[^'])*'|\"(?:\\.|[^\"])*\")", block, re.S):
            context = block[max(0, match.start() - 140):match.start()]
            url = decode_js_literal(match.group(1))
            if "watermark_info" in context or "share_cover" in context:
                continue
            if "from=appmsg" in url or "mmbiz.qpic.cn" in urllib.parse.urlparse(url).netloc:
                urls.append(url)

    if not urls:
        for attr in ["data-src", "src"]:
            for match in re.finditer(rf'{attr}="(https?://[^"]+)"', page_html, re.I):
                url = html_lib.unescape(match.group(1))
                if "mmbiz.qpic.cn" in urllib.parse.urlparse(url).netloc:
                    urls.append(url)

    deduped: list[str] = []
    seen: set[str] = set()
    for url in urls:
        key = url.split("#", 1)[0]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(url)
    return deduped


def sanitize_filename(name: str, fallback: str = "weixin-article") -> str:
    cleaned = re.sub(r'[\\/:*?"<>|\x00-\x1f]', " ", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" .")
    return cleaned[:120] or fallback


def extension_for(url: str, content_type: str) -> str:
    query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    fmt = (query.get("wx_fmt") or query.get("tp") or [""])[0].lower()
    if fmt in {"jpeg", "jpg"}:
        return ".jpg"
    if fmt in {"png", "gif", "webp"}:
        return f".{fmt}"
    guessed = mimetypes.guess_extension(content_type.split(";", 1)[0].strip())
    if guessed == ".jpe":
        return ".jpg"
    return guessed or ".png"


def run_opencli(url: str) -> tuple[str | None, dict[str, object]]:
    summary: dict[str, object] = {"available": bool(shutil.which("opencli")), "ran": False}
    if not summary["available"]:
        return None, summary

    with tempfile.TemporaryDirectory(prefix="weixin-opencli-") as temp_dir:
        command = [
            "opencli",
            "weixin",
            "download",
            "--url",
            url,
            "--output",
            temp_dir,
            "--download-images",
            "true",
            "-f",
            "yaml",
        ]
        result = subprocess.run(command, text=True, capture_output=True)
        summary.update(
            {
                "ran": True,
                "returncode": result.returncode,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        )
        if result.returncode != 0:
            return None, summary
        markdown_files = sorted(Path(temp_dir).rglob("*.md"))
        if not markdown_files:
            return None, summary
        summary["markdown"] = str(markdown_files[0])
        return markdown_files[0].read_text(encoding="utf-8", errors="replace"), summary


def clean_opencli_markdown(markdown: str | None, title: str) -> str:
    if not markdown:
        return ""
    drop_contains = [
        "原文链接",
        "继续滑动看下一个",
        "向上滑动看下一个",
        "喜欢此内容的人还喜欢",
        "赞赏",
        "微信扫一扫",
    ]
    lines: list[str] = []
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if line.startswith("# ") and clean_text(line[2:]) == title:
            continue
        if line.startswith("> "):
            continue
        if line.startswith("![") or line.startswith("![["):
            continue
        if any(token in line for token in drop_contains):
            continue
        lines.append(line)
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines).strip()


def write_markdown(
    md_path: Path,
    title: str,
    account: str,
    publish_time: str,
    url: str,
    body: str,
    image_refs: list[str],
    locale: str,
    overwrite: bool,
) -> None:
    if md_path.exists() and not overwrite:
        raise SystemExit(f"Refusing to overwrite existing note: {md_path}")
    labels = {
        "zh": ("公众号", "发布时间", "原文链接"),
        "en": ("Account", "Published", "Source URL"),
    }[locale]
    lines = [f"# {title}", ""]
    if account:
        lines.append(f"> {labels[0]}：{account}" if locale == "zh" else f"> {labels[0]}: {account}")
    if publish_time:
        lines.append(f"> {labels[1]}：{publish_time}" if locale == "zh" else f"> {labels[1]}: {publish_time}")
    lines.append(f"> {labels[2]}：{url}" if locale == "zh" else f"> {labels[2]}: {url}")
    lines.append("")
    if body:
        lines.append(body)
        lines.append("")
    for ref in image_refs:
        lines.append(f"![[{ref}]]")
        lines.append("")
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Save a Weixin article into an Obsidian vault.")
    parser.add_argument("url", help="mp.weixin.qq.com article URL")
    parser.add_argument("--vault-root", default=os.getcwd(), help="Obsidian vault root")
    parser.add_argument("--target-dir", default="", help="Relative note directory inside the vault")
    parser.add_argument("--title", default="", help="Override article title")
    parser.add_argument("--locale", choices=["zh", "en"], default="zh", help="Metadata label language")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing note")
    parser.add_argument("--max-images", type=int, default=0, help="Limit downloaded images; 0 means all")
    args = parser.parse_args()

    vault_root = Path(args.vault_root).expanduser().resolve()
    target_dir = (vault_root / args.target_dir).resolve()
    try:
        target_dir.relative_to(vault_root)
    except ValueError:
        raise SystemExit("--target-dir must stay inside --vault-root")

    opencli_markdown, opencli_summary = run_opencli(args.url)
    page_html = fetch_text(args.url)
    title = sanitize_filename(args.title or extract_title(page_html))
    account = extract_author(page_html)
    publish_time = extract_publish_time(page_html)
    opencli_body = clean_opencli_markdown(opencli_markdown, title)
    body = extract_body_text(page_html, opencli_body)

    image_urls = extract_picture_urls(page_html)
    if args.max_images > 0:
        image_urls = image_urls[: args.max_images]

    asset_dir = vault_root / "assets" / title
    asset_dir.mkdir(parents=True, exist_ok=True)
    image_refs: list[str] = []
    for index, image_url in enumerate(image_urls, start=1):
        data, content_type = fetch_bytes(image_url, referer=args.url)
        ext = extension_for(image_url, content_type)
        filename = f"{title}-{index:02d}{ext}"
        image_path = asset_dir / filename
        image_path.write_bytes(data)
        image_refs.append(f"assets/{title}/{filename}")

    md_path = target_dir / f"{title}.md"
    write_markdown(
        md_path=md_path,
        title=title,
        account=account,
        publish_time=publish_time,
        url=args.url,
        body=body,
        image_refs=image_refs,
        locale=args.locale,
        overwrite=args.overwrite,
    )

    summary = {
        "note": str(md_path),
        "assets": str(asset_dir),
        "images": len(image_refs),
        "title": title,
        "account": account,
        "publish_time": publish_time,
        "opencli": opencli_summary,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
