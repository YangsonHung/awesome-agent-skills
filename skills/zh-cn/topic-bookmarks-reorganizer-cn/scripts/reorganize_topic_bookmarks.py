#!/usr/bin/env python3
"""Reorganize one topic folder from Netscape bookmarks export into cleaner categories."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import OrderedDict, Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

H3_RE = re.compile(r'^(?P<indent>\s*)<DT><H3(?P<attrs>[^>]*)>(?P<title>.*?)</H3>\s*$')
A_RE = re.compile(r'^(?P<indent>\s*)<DT><A\s+(?P<attrs>[^>]*)>(?P<title>.*?)</A>\s*$')
HREF_RE = re.compile(r'HREF="([^"]+)"', re.IGNORECASE)

LANG_LABELS = {
    "zh": {
        "coding": "01 编程开发",
        "platform": "02 模型与平台",
        "agent": "03 Agent与协议自动化",
        "design": "04 设计与多媒体",
        "learning": "05 学习与内容",
        "nav": "06 榜单与导航",
        "account": "07 商业与账号",
        "ops": "08 工具与平台",
        "community": "09 社区与讨论",
        "backlog": "99 待整理",
        "uncategorized": "未分类",
    },
    "en": {
        "coding": "01 Coding Development",
        "platform": "02 Models Platforms",
        "agent": "03 Agent Protocol Automation",
        "design": "04 Design Multimedia",
        "learning": "05 Learning Content",
        "nav": "06 Rankings Navigation",
        "account": "07 Commercial Accounts",
        "ops": "08 Tools Platforms",
        "community": "09 Community Discussion",
        "backlog": "99 Backlog",
        "uncategorized": "Uncategorized",
    },
}


AI_CODING_SECTIONS = {
    "CLI", "Copilot", "Cursor", "kat-coder", "长亭百智云-MonkeyCode", "claude-cowork", "ZenMux",
}

AI_PLATFORM_SECTIONS = {
    "Anthropic", "OpenAI", "智谱AI", "mini max", "Google", "Manus", "DeepSeek", "Grok", "Qwen",
    "Moonshot", "豆包", "Poe", "OpenRouter", "Perplexxity", "腾讯元宝", "心流", "昆仑万维",
    "夸克", "character AI",
}

AI_AGENT_SECTIONS = {"扣子", "火山方舟", "anyrouter", "n8n", "dify", "lovable", "teamo"}
AI_DESIGN_SECTIONS = {"AI 设计", "即梦", "comfy", "海螺", "labnana"}

AI_TOP_AGENT = {"OpenClaw", "AI Chatbot", "AI 协议", "Agent Skills", "mcp"}
AI_TOP_DESIGN = {"AI PDF", "AI 内容生产"}
AI_TOP_LEARNING = {"Course", "社区", "prompt", "SDD"}
AI_TOP_NAV = {"Arena", "排行榜", "导航网"}
AI_TOP_ACCOUNT = {"代充"}
AI_TOP_CODING = {"OneCode"}
AI_TOP_BACKLOG = {"todo"}

GENERIC_KEYWORDS = {
    "coding": ["code", "coding", "program", "developer", "github", "gitlab", "api", "sdk", "cli", "terminal", "编程", "开发"],
    "learning": ["course", "tutorial", "guide", "learn", "docs", "blog", "wiki", "知乎", "掘金", "教程", "文档"],
    "agent": ["agent", "workflow", "automation", "protocol", "mcp", "自动化", "协议", "智能体"],
    "design": ["design", "image", "video", "pdf", "图像", "视频", "设计"],
    "nav": ["leaderboard", "ranking", "navigation", "directory", "榜", "导航"],
    "account": ["billing", "subscription", "recharge", "pay", "充值", "订阅", "账号"],
    "community": ["community", "forum", "discord", "reddit", "讨论", "社区"],
    "ops": ["cloud", "console", "platform", "dashboard", "workspace", "控制台", "平台"],
}


@dataclass
class LinkEntry:
    href: str
    attrs: str
    title_raw: str
    title_dec: str
    path: List[str]
    mapped_path: List[str] = field(default_factory=list)


@dataclass
class TreeNode:
    folders: OrderedDict = field(default_factory=OrderedDict)
    links: List[LinkEntry] = field(default_factory=list)


def decode_text(value: str) -> str:
    return html.unescape(value).strip()


def find_topic_range(lines: List[str], topic_folder: str) -> tuple[int, int, int]:
    start = -1
    topic_indent = -1
    target = topic_folder.strip().casefold()

    for idx, line in enumerate(lines):
        m = H3_RE.match(line)
        if not m:
            continue
        title = decode_text(m.group("title"))
        if title.casefold() == target:
            start = idx
            topic_indent = len(m.group("indent"))
            break

    if start < 0:
        raise ValueError(f"Topic folder '{topic_folder}' not found")

    end = len(lines) - 1
    for idx in range(start + 1, len(lines)):
        m = H3_RE.match(lines[idx])
        if not m:
            continue
        if len(m.group("indent")) == topic_indent:
            end = idx - 1
            break

    return start, end, topic_indent


def parse_topic_entries(lines: List[str], start: int, end: int) -> List[LinkEntry]:
    entries: List[LinkEntry] = []
    stack: Dict[int, str] = {}

    for idx in range(start, end + 1):
        line = lines[idx]

        h3 = H3_RE.match(line)
        if h3:
            indent = len(h3.group("indent"))
            title_dec = decode_text(h3.group("title"))
            for key in list(stack.keys()):
                if key >= indent:
                    del stack[key]
            stack[indent] = title_dec
            continue

        a = A_RE.match(line)
        if not a:
            continue

        indent = len(a.group("indent"))
        attrs = a.group("attrs")
        title_raw = a.group("title")
        title_dec = decode_text(title_raw)
        href_match = HREF_RE.search(attrs)
        href = href_match.group(1).strip() if href_match else ""

        path = [v for k, v in sorted(stack.items()) if k < indent]
        if not path:
            continue

        entries.append(
            LinkEntry(
                href=href,
                attrs=attrs,
                title_raw=title_raw,
                title_dec=title_dec,
                path=path,
            )
        )

    return entries


def map_ai_path(rel: List[str], labels: Dict[str, str]) -> List[str]:
    if not rel:
        return [labels["backlog"], labels["uncategorized"]]

    top = rel[0]

    if top == "工具":
        sec = rel[1] if len(rel) > 1 else "工具-未分类"
        rest = rel[2:] if len(rel) > 2 else []

        if sec in AI_CODING_SECTIONS:
            bucket = "coding"
        elif sec in AI_PLATFORM_SECTIONS:
            bucket = "platform"
        elif sec in AI_AGENT_SECTIONS:
            bucket = "agent"
        elif sec in AI_DESIGN_SECTIONS:
            bucket = "design"
        elif sec == "New folder":
            bucket = "backlog"
        else:
            bucket = "platform"

        return [labels[bucket], sec] + rest

    if top in AI_TOP_AGENT:
        return [labels["agent"], top] + rel[1:]
    if top in AI_TOP_DESIGN:
        return [labels["design"], top] + rel[1:]
    if top in AI_TOP_LEARNING:
        return [labels["learning"], top] + rel[1:]
    if top in AI_TOP_NAV:
        return [labels["nav"], top] + rel[1:]
    if top in AI_TOP_ACCOUNT:
        return [labels["account"], top] + rel[1:]
    if top in AI_TOP_CODING:
        return [labels["coding"], top] + rel[1:]
    if top in AI_TOP_BACKLOG:
        return [labels["backlog"], top] + rel[1:]

    return [labels["backlog"], top] + rel[1:]


def classify_generic(entry: LinkEntry, labels: Dict[str, str]) -> str:
    haystack = " ".join(entry.path + [entry.title_dec, entry.href]).casefold()

    for bucket, words in GENERIC_KEYWORDS.items():
        if any(word in haystack for word in words):
            return labels[bucket]

    return labels["ops"]


def map_generic_path(rel: List[str], entry: LinkEntry, labels: Dict[str, str]) -> List[str]:
    top = rel[0] if rel else labels["uncategorized"]
    bucket = classify_generic(entry, labels)
    return [bucket, top] + rel[1:]


def map_entries(entries: List[LinkEntry], topic_folder: str, mode: str, lang: str) -> tuple[List[LinkEntry], str]:
    labels = LANG_LABELS[lang]

    if mode == "auto":
        topic_cf = topic_folder.casefold()
        selected = "ai" if ("ai" in topic_cf or "智能" in topic_cf) else "generic"
    else:
        selected = mode

    for entry in entries:
        rel = entry.path[1:] if len(entry.path) > 1 else []
        if selected == "ai":
            entry.mapped_path = map_ai_path(rel, labels)
        else:
            entry.mapped_path = map_generic_path(rel, entry, labels)

    return entries, selected


def dedupe_entries(entries: List[LinkEntry], dedupe_url: bool) -> tuple[List[LinkEntry], int]:
    if not dedupe_url:
        return entries, 0

    seen = set()
    result: List[LinkEntry] = []
    removed = 0

    for entry in entries:
        href = entry.href.strip()
        if href and href in seen:
            removed += 1
            continue
        if href:
            seen.add(href)
        result.append(entry)

    return result, removed


def insert_tree(root: TreeNode, entry: LinkEntry) -> None:
    node = root
    for segment in entry.mapped_path:
        if segment not in node.folders:
            node.folders[segment] = TreeNode()
        node = node.folders[segment]
    node.links.append(entry)


def render_tree(node: TreeNode, indent: int, preferred: List[str]) -> List[str]:
    lines: List[str] = []
    keys = list(node.folders.keys())
    ordered = [k for k in preferred if k in node.folders] + [k for k in keys if k not in preferred]

    for name in ordered:
        child = node.folders[name]
        sp = " " * indent
        lines.append(f"{sp}<DT><H3>{html.escape(name)}</H3>")
        lines.append(f"{sp}<DL><p>")
        lines.extend(render_tree(child, indent + 4, preferred=[]))
        for link in child.links:
            lines.append(f"{sp}    <DT><A {link.attrs}>{link.title_raw}</A>")
        lines.append(f"{sp}</DL><p>")

    return lines


def build_output(topic_folder: str, root: TreeNode, mode: str, lang: str) -> str:
    labels = LANG_LABELS[lang]

    if mode == "ai":
        preferred = [
            labels["coding"], labels["platform"], labels["agent"], labels["design"],
            labels["learning"], labels["nav"], labels["account"], labels["backlog"],
        ]
    else:
        preferred = [
            labels["coding"], labels["platform"], labels["agent"], labels["design"],
            labels["learning"], labels["community"], labels["nav"], labels["account"],
            labels["ops"], labels["backlog"],
        ]

    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        "<!-- This is an automatically generated file.",
        "     It will be read and overwritten.",
        "     DO NOT EDIT! -->",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>Bookmarks</TITLE>",
        "<H1>Bookmarks</H1>",
        "<DL><p>",
        f"    <DT><H3>{html.escape(topic_folder)}</H3>",
        "    <DL><p>",
    ]

    lines.extend(render_tree(root, indent=12, preferred=preferred))

    lines.extend([
        "    </DL><p>",
        "</DL><p>",
    ])

    return "\n".join(lines) + "\n"


def collect_report(topic_folder: str, entries_before: List[LinkEntry], entries_after: List[LinkEntry], removed_duplicates: int, selected_mode: str) -> Dict:
    original_top = Counter()
    mapped_top = Counter()
    domains = Counter()

    for entry in entries_before:
        rel = entry.path[1:] if len(entry.path) > 1 else []
        key = rel[0] if rel else "(direct)"
        original_top[key] += 1

    for entry in entries_after:
        if entry.mapped_path:
            mapped_top[entry.mapped_path[0]] += 1
        if entry.href:
            host = urlparse(entry.href).hostname or ""
            host = host.lower().removeprefix("www.")
            if host:
                domains[host] += 1

    return {
        "topic_folder": topic_folder,
        "selected_mode": selected_mode,
        "input_links": len(entries_before),
        "output_links": len(entries_after),
        "removed_duplicates": removed_duplicates,
        "original_top_level_counts": dict(original_top.most_common()),
        "output_category_counts": dict(mapped_top.most_common()),
        "top_domains": dict(domains.most_common(20)),
    }


def print_report(report: Dict) -> None:
    print("topic:", report["topic_folder"])
    print("mode:", report["selected_mode"])
    print("input_links:", report["input_links"])
    print("output_links:", report["output_links"])
    print("removed_duplicates:", report["removed_duplicates"])

    print("\noriginal_top_level_counts:")
    for k, v in report["original_top_level_counts"].items():
        print(f"  {k}: {v}")

    print("\noutput_category_counts:")
    for k, v in report["output_category_counts"].items():
        print(f"  {k}: {v}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Reorganize one topic folder from browser bookmarks export")
    parser.add_argument("--input", required=True, help="Path to source bookmarks HTML")
    parser.add_argument("--output", required=True, help="Path to output bookmarks HTML")
    parser.add_argument("--topic-folder", default="AI", help="Folder title to extract and reorganize")
    parser.add_argument("--mode", choices=["auto", "ai", "generic"], default="auto", help="Mapping strategy")
    parser.add_argument("--lang", choices=["zh", "en"], default="zh", help="Output category label language")
    parser.add_argument("--no-dedupe-url", action="store_true", help="Do not deduplicate same URL")
    parser.add_argument("--report", help="Write JSON report path")
    parser.add_argument("--print-report", action="store_true", help="Print report to console")
    args = parser.parse_args()

    source = Path(args.input)
    output = Path(args.output)

    if not source.exists():
        raise SystemExit(f"Input file not found: {source}")

    lines = source.read_text(encoding="utf-8", errors="ignore").splitlines()
    start, end, _ = find_topic_range(lines, args.topic_folder)

    entries = parse_topic_entries(lines, start, end)
    if not entries:
        raise SystemExit(f"No links found under topic folder '{args.topic_folder}'")

    entries, selected_mode = map_entries(entries, args.topic_folder, args.mode, args.lang)
    entries_out, removed = dedupe_entries(entries, dedupe_url=not args.no_dedupe_url)

    root = TreeNode()
    for entry in entries_out:
        insert_tree(root, entry)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_output(args.topic_folder, root, selected_mode, args.lang), encoding="utf-8")

    report = collect_report(args.topic_folder, entries, entries_out, removed, selected_mode)
    if args.report:
        report_path = Path(args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.print_report:
        print_report(report)


if __name__ == "__main__":
    main()
