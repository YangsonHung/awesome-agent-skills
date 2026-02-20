#!/usr/bin/env python3
"""Convert chat-export JSON into one Markdown file per conversation."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


Turn = tuple[str, str]
Conversation = dict[str, Any]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert chat-export JSON records to multiple Markdown files. "
            "Supports mapping/fragments, role-content message lists, and common QA pair formats."
        )
    )
    parser.add_argument("--input", required=True, help="Path to user-provided JSON file")
    parser.add_argument("--output-dir", required=True, help="Directory to write markdown files")
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove existing *.md files in output directory before writing",
    )
    return parser.parse_args()


def to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    if isinstance(value, list):
        parts = [to_text(item).strip() for item in value]
        parts = [part for part in parts if part]
        return "\n".join(parts)
    if isinstance(value, dict):
        for key in (
            "text",
            "value",
            "content",
            "message",
            "output",
            "answer",
            "prompt",
            "question",
        ):
            if key in value:
                text = to_text(value.get(key)).strip()
                if text:
                    return text
        if "parts" in value:
            text = to_text(value.get("parts")).strip()
            if text:
                return text
    return json.dumps(value, ensure_ascii=False, indent=2)


def clean_filename(raw: str, max_len: int = 120) -> str:
    text = (raw or "").strip() or "未命名会话"
    text = re.sub(r'[\\/:*?"<>|\r\n\t]+', " ", text)
    text = re.sub(r"\s+", " ", text).strip(" .")
    text = text[:max_len].rstrip(" .")
    return text or "未命名会话"


def question_heading(raw: str) -> str:
    single_line = re.sub(r"\s+", " ", (raw or "").strip())
    return single_line or "（空问题）"


def demote_response_headings(markdown: str) -> str:
    """Demote headings by one level while preserving fenced code blocks."""
    lines = markdown.splitlines()
    result: list[str] = []
    in_code_block = False
    for line in lines:
        if re.match(r"^\s*```", line):
            in_code_block = not in_code_block
            result.append(line)
            continue
        if in_code_block:
            result.append(line)
            continue
        match = re.match(r"^(\s*)(#{1,6})(\s+.*)$", line)
        if not match:
            result.append(line)
            continue
        indent, hashes, rest = match.groups()
        level = min(6, len(hashes) + 1)
        result.append(f"{indent}{'#' * level}{rest}")
    return "\n".join(result).strip()


def normalize_role(raw: Any) -> str | None:
    if raw is None:
        return None
    role = str(raw).strip().lower()
    if not role:
        return None
    mapping = {
        "user": "user",
        "human": "user",
        "request": "user",
        "question": "user",
        "prompt": "user",
        "assistant": "assistant",
        "bot": "assistant",
        "gpt": "assistant",
        "response": "assistant",
        "answer": "assistant",
        "model": "assistant",
        "system": "system",
    }
    if role in mapping:
        return mapping[role]
    if "assistant" in role or "model" in role:
        return "assistant"
    if "user" in role or "human" in role:
        return "user"
    return None


def extract_role_from_message(message: dict[str, Any]) -> str | None:
    role_candidates = [
        message.get("role"),
        message.get("from"),
        message.get("sender"),
        message.get("author_role"),
        message.get("type"),
    ]
    author = message.get("author")
    if isinstance(author, dict):
        role_candidates.append(author.get("role"))
    for candidate in role_candidates:
        normalized = normalize_role(candidate)
        if normalized:
            return normalized
    if message.get("is_user") is True or message.get("isUser") is True:
        return "user"
    if message.get("is_assistant") is True:
        return "assistant"
    return None


def extract_content_from_content_list(content_list: Any, role: str | None) -> str:
    if not isinstance(content_list, list):
        return ""

    preferred: list[str] = []
    fallback: list[str] = []
    skipped_phases = {"think", "reasoning", "web_search", "search"}

    for item in content_list:
        phase = ""
        item_role: str | None = None
        text = ""

        if isinstance(item, dict):
            phase = str(item.get("phase") or "").strip().lower()
            item_role = normalize_role(item.get("role"))

            for key in ("content", "text", "value", "message", "output", "answer"):
                if key not in item:
                    continue
                candidate = to_text(item.get(key)).strip()
                if candidate:
                    text = candidate
                    break
        else:
            text = to_text(item).strip()

        if not text:
            continue

        if role == "assistant":
            if item_role == "function":
                continue
            if phase in {"answer", "final", "output", "response"}:
                preferred.append(text)
                continue
            if phase in skipped_phases:
                continue

        fallback.append(text)

    if preferred:
        return "\n\n".join(preferred).strip()
    return "\n\n".join(fallback).strip()


def extract_text_from_content_blocks(blocks: Any, role: str | None) -> str:
    if not isinstance(blocks, list):
        return ""

    preferred: list[str] = []
    fallback: list[str] = []
    skip_types = {"thinking", "tool_use", "tool_result", "token_budget", "search_result", "search_results"}

    for item in blocks:
        if isinstance(item, str):
            text = item.strip()
            if text:
                fallback.append(text)
            continue

        if not isinstance(item, dict):
            continue

        block_type = str(item.get("type") or "").strip().lower()
        if block_type in skip_types:
            continue

        text = ""
        for key in ("text", "content", "value", "message"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                text = value.strip()
                break

        if not text:
            continue

        if block_type in {"text", "markdown"}:
            preferred.append(text)
        else:
            # For unknown block types, keep as fallback (helps compatibility with future exports).
            fallback.append(text)

    if preferred:
        return "\n\n".join(preferred).strip()
    return "\n\n".join(fallback).strip()


def extract_content_from_message(message: dict[str, Any], role: str | None) -> str:
    content_value = message.get("content")
    if isinstance(content_value, list):
        text = extract_text_from_content_blocks(content_value, role).strip()
        if text:
            return text
    elif content_value is not None:
        text = to_text(content_value).strip()
        if text:
            return text

    for key in ("text", "value", "message", "output", "answer", "prompt", "question"):
        if key in message:
            text = to_text(message.get(key)).strip()
            if text:
                return text
    if "content_list" in message:
        text = extract_content_from_content_list(message.get("content_list"), role).strip()
        if text:
            return text
    if role == "assistant":
        text = to_text(message.get("reasoning_content")).strip()
        if text:
            return text
    return ""


def extract_pair_turns(entry: dict[str, Any]) -> list[Turn]:
    pair_keys = [
        ("question", "answer"),
        ("prompt", "response"),
        ("input", "output"),
        ("instruction", "output"),
        ("request", "response"),
    ]
    for left_key, right_key in pair_keys:
        if left_key in entry and right_key in entry:
            left = to_text(entry.get(left_key)).strip()
            right = to_text(entry.get(right_key)).strip()
            turns: list[Turn] = []
            if left:
                turns.append(("user", left))
            if right:
                turns.append(("assistant", right))
            if turns:
                return turns
    return []


def turns_from_fragments(fragments: list[Any]) -> list[Turn]:
    turns: list[Turn] = []
    for fragment in fragments:
        if not isinstance(fragment, dict):
            continue
        frag_type = str(fragment.get("type") or "").upper()
        content = to_text(fragment.get("content")).strip()
        if not content:
            continue
        if frag_type == "REQUEST":
            turns.append(("user", content))
        elif frag_type == "RESPONSE":
            turns.append(("assistant", content))
    return turns


def turns_from_message(message: Any) -> list[Turn]:
    if isinstance(message, dict):
        fragments = message.get("fragments")
        if isinstance(fragments, list):
            turns = turns_from_fragments(fragments)
            if turns:
                return turns

        paired = extract_pair_turns(message)
        if paired:
            return paired

        role = extract_role_from_message(message)
        content = extract_content_from_message(message, role)
        if role in {"user", "assistant"} and content:
            return [(role, content)]
    elif isinstance(message, (list, tuple)) and len(message) >= 2:
        left = to_text(message[0]).strip()
        right = to_text(message[1]).strip()
        turns: list[Turn] = []
        if left:
            turns.append(("user", left))
        if right:
            turns.append(("assistant", right))
        if turns:
            return turns
    return []


def looks_like_message(entry: Any) -> bool:
    if isinstance(entry, dict):
        role_like = any(key in entry for key in ("role", "from", "sender", "author"))
        content_like = any(
            key in entry
            for key in ("content", "text", "value", "message", "fragments", "question", "answer")
        )
        return role_like or content_like
    if isinstance(entry, (list, tuple)) and len(entry) >= 2:
        return True
    return False


def looks_like_message_list(items: Any) -> bool:
    if not isinstance(items, list) or not items:
        return False
    sample = [item for item in items[:20] if item is not None]
    if not sample:
        return False
    matched = sum(1 for item in sample if looks_like_message(item))
    return matched >= max(1, len(sample) // 2)


def node_sort_key(node_id: str, node: dict[str, Any]) -> tuple[Any, ...]:
    message = (node or {}).get("message") or {}
    inserted_at = message.get("inserted_at")
    try:
        numeric_id = int(str(node_id))
    except Exception:
        numeric_id = 10**9
    return (inserted_at is None, inserted_at or "", numeric_id, str(node_id))


def ordered_node_ids(mapping: dict[str, Any]) -> list[str]:
    root = mapping.get("root") or {}
    visited: set[str] = set()
    order: list[str] = []

    def dfs(node_id: str) -> None:
        if node_id in visited:
            return
        visited.add(node_id)
        if node_id != "root" and node_id in mapping:
            order.append(node_id)
        node = mapping.get(node_id) or {}
        for child in node.get("children") or []:
            dfs(str(child))

    for child in root.get("children") or []:
        dfs(str(child))

    remaining = [
        (node_id, node)
        for node_id, node in mapping.items()
        if node_id not in visited and node_id != "root"
    ]
    for node_id, _ in sorted(remaining, key=lambda item: node_sort_key(item[0], item[1])):
        dfs(str(node_id))

    return order


def extract_turns_from_mapping(mapping: dict[str, Any]) -> list[Turn]:
    turns: list[Turn] = []
    for node_id in ordered_node_ids(mapping):
        node = mapping.get(node_id) or {}
        message = node.get("message")
        turns.extend(turns_from_message(message))
    return turns


def extract_turns_from_message_list(messages: list[Any]) -> list[Turn]:
    turns: list[Turn] = []
    for message in messages:
        turns.extend(turns_from_message(message))
    return turns


def history_message_sort_key(item: tuple[str, dict[str, Any]]) -> tuple[Any, ...]:
    message_id, message = item
    for key in ("timestamp", "create_time", "inserted_at", "updated_at"):
        value = message.get(key)
        if value not in (None, ""):
            return (0, value, message_id)
    return (1, "", message_id)


def extract_turns_from_history(history: Any) -> list[Turn]:
    if isinstance(history, list) and looks_like_message_list(history):
        return extract_turns_from_message_list(history)

    if not isinstance(history, dict):
        return []

    messages = history.get("messages")
    if isinstance(messages, list) and looks_like_message_list(messages):
        return extract_turns_from_message_list(messages)

    if not isinstance(messages, dict):
        return []

    # Prefer current path when available.
    current_id = history.get("currentId")
    if isinstance(current_id, str) and current_id in messages:
        chain: list[dict[str, Any]] = []
        seen: set[str] = set()
        cursor: str | None = current_id
        while cursor and cursor not in seen and cursor in messages:
            seen.add(cursor)
            node = messages.get(cursor)
            if isinstance(node, dict):
                chain.append(node)
                parent = node.get("parentId")
                cursor = parent if isinstance(parent, str) and parent else None
            else:
                break
        chain.reverse()
        if chain:
            return extract_turns_from_message_list(chain)

    # Fallback to timestamp/ID order for message map.
    ordered_nodes: list[dict[str, Any]] = [
        node for _, node in sorted(messages.items(), key=history_message_sort_key) if isinstance(node, dict)
    ]
    if ordered_nodes:
        return extract_turns_from_message_list(ordered_nodes)
    return []


def extract_turns_from_chat_container(chat_value: Any) -> list[Turn]:
    if isinstance(chat_value, list) and looks_like_message_list(chat_value):
        return extract_turns_from_message_list(chat_value)

    if not isinstance(chat_value, dict):
        return []

    turns: list[Turn] = []

    messages = chat_value.get("messages")
    if isinstance(messages, list) and looks_like_message_list(messages):
        turns.extend(extract_turns_from_message_list(messages))

    if not turns and "history" in chat_value:
        turns.extend(extract_turns_from_history(chat_value.get("history")))

    # Some exports may store a single message object in chat.
    if not turns and looks_like_message(chat_value):
        turns.extend(turns_from_message(chat_value))

    return turns


def choose_title(obj: dict[str, Any], fallback: str) -> str:
    for key in ("title", "name", "subject", "topic"):
        value = obj.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return fallback


def extract_turns_from_conversation_object(obj: dict[str, Any], fallback_title: str) -> Conversation:
    title = choose_title(obj, fallback_title)
    turns: list[Turn] = []

    mapping = obj.get("mapping")
    if isinstance(mapping, dict):
        turns.extend(extract_turns_from_mapping(mapping))

    for key in ("chat_messages", "messages", "turns", "dialog", "dialogue", "items"):
        value = obj.get(key)
        if isinstance(value, list) and looks_like_message_list(value):
            turns.extend(extract_turns_from_message_list(value))
            break

    if not turns and "history" in obj:
        turns.extend(extract_turns_from_history(obj.get("history")))

    if not turns and "chat" in obj:
        turns.extend(extract_turns_from_chat_container(obj.get("chat")))

    if not turns and "conversation" in obj:
        conv_value = obj.get("conversation")
        if isinstance(conv_value, list) and looks_like_message_list(conv_value):
            turns.extend(extract_turns_from_message_list(conv_value))
        else:
            turns.extend(extract_turns_from_chat_container(conv_value))

    conversations_value = obj.get("conversations")
    if not turns and isinstance(conversations_value, list) and looks_like_message_list(conversations_value):
        turns.extend(extract_turns_from_message_list(conversations_value))

    return {"title": title, "turns": turns}


def normalize_root(data: Any, input_stem: str) -> list[Conversation]:
    conversations: list[Conversation] = []

    if isinstance(data, list):
        if looks_like_message_list(data):
            return [{"title": input_stem, "turns": extract_turns_from_message_list(data)}]
        for index, item in enumerate(data, start=1):
            fallback_title = f"{input_stem}-{index}"
            if isinstance(item, dict):
                conversations.append(extract_turns_from_conversation_object(item, fallback_title))
            elif isinstance(item, list) and looks_like_message_list(item):
                conversations.append({"title": fallback_title, "turns": extract_turns_from_message_list(item)})
        return conversations

    if isinstance(data, dict):
        for key in ("conversations", "data", "items", "chats", "sessions"):
            value = data.get(key)
            if not isinstance(value, list):
                continue
            if looks_like_message_list(value):
                title = choose_title(data, input_stem)
                return [{"title": title, "turns": extract_turns_from_message_list(value)}]

            nested: list[Conversation] = []
            for index, item in enumerate(value, start=1):
                fallback_title = f"{input_stem}-{index}"
                if isinstance(item, dict):
                    nested.append(extract_turns_from_conversation_object(item, fallback_title))
                elif isinstance(item, list) and looks_like_message_list(item):
                    nested.append(
                        {
                            "title": fallback_title,
                            "turns": extract_turns_from_message_list(item),
                        }
                    )
            if nested:
                return nested

        single = extract_turns_from_conversation_object(data, input_stem)
        if single.get("turns"):
            return [single]

        if looks_like_message(data):
            return [{"title": input_stem, "turns": extract_turns_from_message_list([data])}]

    return conversations


def extract_qa_lines(turns: list[Turn]) -> list[str]:
    lines: list[str] = []
    current_question_exists = False

    for role, content in turns:
        body = content.strip()
        if not body:
            continue
        if role == "user":
            lines.append(f"## {question_heading(body)}")
            lines.append("")
            current_question_exists = True
            continue
        if role == "assistant":
            if not current_question_exists:
                lines.append("## （未标注问题）")
                lines.append("")
                current_question_exists = True
            lines.append("### 回答")
            lines.append(demote_response_headings(body) or "（无回答内容）")
            lines.append("")

    return lines


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with input_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    normalized = normalize_root(data, input_path.stem)
    if not normalized:
        raise ValueError(
            "Cannot detect a supported conversation structure in input JSON. "
            "Please provide a sample format so the parser can be extended."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    if args.clean:
        for md_file in output_dir.glob("*.md"):
            md_file.unlink()

    name_counter: defaultdict[str, int] = defaultdict(int)
    written = 0
    exported_with_qa = 0

    for index, conversation in enumerate(normalized, start=1):
        raw_title = (conversation.get("title") or "").strip() or f"{input_path.stem}-{index}"
        base_name = clean_filename(raw_title)
        name_counter[base_name] += 1
        duplicate_index = name_counter[base_name]
        filename = f"{base_name}.md" if duplicate_index == 1 else f"{base_name} ({duplicate_index}).md"

        turns = conversation.get("turns") or []
        qa_lines = extract_qa_lines(turns)
        lines = [f"# {raw_title}", ""]
        if qa_lines:
            lines.extend(qa_lines)
            exported_with_qa += 1
        else:
            lines.append("（无可导出的问答内容）")
            lines.append("")

        (output_dir / filename).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        written += 1

    print(f"Detected conversations: {len(normalized)}")
    print(f"Converted files: {written}")
    print(f"Files with Q/A content: {exported_with_qa}")
    print(f"Output directory: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
