---
name: conversation-json-to-md
description: Convert chat export JSON files into multiple Markdown files (one conversation per file). Use when users ask to split AI chat logs, preserve only user-assistant Q/A, format question as heading, keep response Markdown, and normalize filenames/headings after export.
risk: safe
source: YangsonHung/awesome-agent-skills
---

# Conversation JSON To MD

Convert a user-provided chat-export JSON into multiple Markdown files with consistent Q/A formatting.

## When to Use

Use this skill when the user asks for:
- Splitting one JSON chat export into many `.md` files
- One conversation per markdown file
- Keeping only question/answer content from user and assistant
- Renaming response section to `回答`
- Normalizing exported files with a second formatting pass

## Do not use

Do not use this skill for:
- Plain text transformation that does not involve JSON chat exports
- Non-conversation JSON processing tasks
- Requests requiring semantic summarization instead of structural conversion

## Instructions

1. Read the input file path provided by the user. Do not assume default file names.
2. Detect conversation/message structure automatically.
3. Export one markdown file per conversation.
4. Keep only user/assistant Q&A content.
5. Format each Q/A block as:
   - `## <question text>`
   - `### 回答`
6. Preserve answer markdown and demote answer-internal heading levels by one level.
7. Run an independent second-pass formatting check and fix naming/title structure before final delivery.

## Supported Input Structures

The bundled script supports common export formats including:
- DeepSeek/ChatGPT-like mapping tree (`mapping/root/children/fragments`)
- Qwen-like exports (`data[].chat.messages[]`, `content_list` with `phase=answer`)
- Claude web export style (`list[{ name, chat_messages: [...] }]`)
- Generic message arrays (`messages`, `history`, `conversations`, `dialog`, `turns`)
- Pair fields (`question-answer`, `prompt-response`, `input-output`)

If format detection fails, stop and ask the user for a sample snippet, then extend parsing rules.

## Run Script

```bash
python3 scripts/convert_conversations.py \
  --input /path/to/<user-provided>.json \
  --output-dir /path/to/output_md \
  --clean
```

## Output Format

Each output file uses this structure:

```md
# <conversation title>

## <user question 1>
### 回答
<assistant answer markdown>

## <user question 2>
### 回答
<assistant answer markdown>
```

## Second-Pass Formatting (Required)

After export, run a second-pass check/fix on output files:

1. Filename normalization:
- Keep title-only naming
- Remove illegal filename characters
- Resolve duplicates with ` (2)`, ` (3)`...

2. Heading normalization:
- Keep only one H1: `# <conversation title>`
- Ensure questions are H2
- Ensure responses are exactly `### 回答`

3. Body normalization:
- Keep answer body markdown
- Keep answer-internal heading demotion

4. Final verification:
- Confirm no files still violate naming or heading rules

## Validation Checklist

- File count equals detected conversation count
- No random suffixes in filenames
- No `## REQUEST` or `## RESPONSE` headers in output
- Response blocks are present as `### 回答`
- Output preserves markdown rendering correctly
