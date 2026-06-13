const fs = require('fs');
const path = require('path');

function stripQuotes(value) {
  if (typeof value !== 'string') return value;
  if (value.length < 2) return value.trim();
  const first = value[0];
  const last = value[value.length - 1];
  if ((first === '"' && last === '"') || (first === "'" && last === "'")) {
    return value.slice(1, -1).trim();
  }
  if (first === '"' || first === "'") {
    return value.slice(1).trim();
  }
  if (last === '"' || last === "'") {
    return value.slice(0, -1).trim();
  }
  return value.trim();
}

function parseInlineList(raw) {
  if (typeof raw !== 'string') return [];
  const value = raw.trim();
  if (!value.startsWith('[') || !value.endsWith(']')) return [];
  const inner = value.slice(1, -1).trim();
  if (!inner) return [];
  return inner
    .split(',')
    .map(item => stripQuotes(item.trim()))
    .filter(Boolean);
}

function isPlainObject(value) {
  return value && typeof value === 'object' && !Array.isArray(value);
}

function parseScalar(value) {
  const trimmed = value.trim();
  if (!trimmed) return '';
  if (trimmed.startsWith('[') && trimmed.endsWith(']')) {
    return parseInlineList(trimmed);
  }
  if (trimmed === 'true') return true;
  if (trimmed === 'false') return false;
  return stripQuotes(trimmed);
}

function countIndent(line) {
  const match = line.match(/^ */);
  return match ? match[0].length : 0;
}

function parseBlockScalar(lines, startIndex, mode) {
  const blockLines = [];
  let i = startIndex;
  while (i < lines.length) {
    const line = lines[i];
    if (line.trim() && countIndent(line) === 0) break;
    blockLines.push(line.replace(/^ {1,}/, ''));
    i += 1;
  }
  const value = mode.startsWith('|')
    ? blockLines.join('\n').trim()
    : blockLines.map(line => line.trim()).filter(Boolean).join(' ');
  return { value, nextIndex: i };
}

function parseNestedMapping(lines, startIndex) {
  const value = {};
  const errors = [];
  let i = startIndex;
  while (i < lines.length) {
    const line = lines[i];
    if (!line.trim()) {
      i += 1;
      continue;
    }
    if (countIndent(line) === 0) break;
    const match = line.trim().match(/^([A-Za-z0-9_-]+):(?:\s*(.*))?$/);
    if (!match) {
      errors.push(`Unsupported nested frontmatter line: ${line}`);
      i += 1;
      continue;
    }
    value[match[1]] = parseScalar(match[2] || '');
    i += 1;
  }
  return { value, errors, nextIndex: i };
}

function parseSimpleYamlMapping(fmText) {
  const lines = fmText.split(/\r?\n/);
  const data = {};
  const errors = [];

  for (let i = 0; i < lines.length;) {
    const line = lines[i];
    if (!line.trim() || line.trim().startsWith('#')) {
      i += 1;
      continue;
    }
    if (countIndent(line) > 0) {
      errors.push(`Unexpected indented frontmatter line: ${line}`);
      i += 1;
      continue;
    }

    const match = line.match(/^([A-Za-z0-9_-]+):(?:\s*(.*))?$/);
    if (!match) {
      errors.push(`Unsupported frontmatter line: ${line}`);
      i += 1;
      continue;
    }

    const key = match[1];
    const rawValue = match[2] || '';
    const trimmedValue = rawValue.trim();
    if (trimmedValue.startsWith('|') || trimmedValue.startsWith('>')) {
      const parsed = parseBlockScalar(lines, i + 1, trimmedValue);
      data[key] = parsed.value;
      i = parsed.nextIndex;
      continue;
    }
    if (!trimmedValue && i + 1 < lines.length && countIndent(lines[i + 1]) > 0) {
      const parsed = parseNestedMapping(lines, i + 1);
      data[key] = parsed.value;
      errors.push(...parsed.errors);
      i = parsed.nextIndex;
      continue;
    }

    data[key] = parseScalar(trimmedValue);
    i += 1;
  }

  return { data, errors };
}

function parseFrontmatter(content) {
  const sanitized = content.replace(/^\uFEFF/, '');
  const lines = sanitized.split(/\r?\n/);
  if (!lines.length || lines[0].trim() !== '---') {
    return { data: {}, body: content, errors: [], hasFrontmatter: false };
  }

  let endIndex = -1;
  for (let i = 1; i < lines.length; i += 1) {
    if (lines[i].trim() === '---') {
      endIndex = i;
      break;
    }
  }

  if (endIndex === -1) {
    return {
      data: {},
      body: content,
      errors: ['Missing closing frontmatter delimiter (---).'],
      hasFrontmatter: true,
    };
  }

  const errors = [];
  const fmText = lines.slice(1, endIndex).join('\n');
  const parsed = parseSimpleYamlMapping(fmText);
  let data = parsed.data;
  errors.push(...parsed.errors);

  if (!isPlainObject(data)) {
    errors.push('Frontmatter must be a YAML mapping/object.');
    data = {};
  }

  const body = lines.slice(endIndex + 1).join('\n');
  return { data, body, errors, hasFrontmatter: true };
}

function tokenize(value) {
  if (!value) return [];
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .split(' ')
    .map(token => token.trim())
    .filter(Boolean);
}

function unique(list) {
  const seen = new Set();
  const result = [];
  for (const item of list) {
    if (!item || seen.has(item)) continue;
    seen.add(item);
    result.push(item);
  }
  return result;
}

function readSkill(skillDir, skillId) {
  const skillPath = path.join(skillDir, skillId, 'SKILL.md');
  const content = fs.readFileSync(skillPath, 'utf8');
  const { data } = parseFrontmatter(content);
  const name = typeof data.name === 'string' && data.name.trim()
    ? data.name.trim()
    : skillId;
  const description = typeof data.description === 'string'
    ? data.description.trim()
    : '';

  let tags = [];
  if (Array.isArray(data.tags)) {
    tags = data.tags.map(tag => String(tag).trim());
  } else if (typeof data.tags === 'string' && data.tags.trim()) {
    const parts = data.tags.includes(',')
      ? data.tags.split(',')
      : data.tags.split(/\s+/);
    tags = parts.map(tag => tag.trim());
  } else if (isPlainObject(data.metadata) && data.metadata.tags) {
    const rawTags = data.metadata.tags;
    if (Array.isArray(rawTags)) {
      tags = rawTags.map(tag => String(tag).trim());
    } else if (typeof rawTags === 'string' && rawTags.trim()) {
      const parts = rawTags.includes(',')
        ? rawTags.split(',')
        : rawTags.split(/\s+/);
      tags = parts.map(tag => tag.trim());
    }
  }

  tags = tags.filter(Boolean);

  return {
    id: skillId,
    name,
    description,
    tags,
    path: skillPath,
    content,
  };
}

function listSkillIds(skillsDir) {
  return fs.readdirSync(skillsDir)
    .filter(entry => {
      if (entry.startsWith('.')) return false;
      const dirPath = path.join(skillsDir, entry);
      if (!fs.statSync(dirPath).isDirectory()) return false;
      const skillPath = path.join(dirPath, 'SKILL.md');
      return fs.existsSync(skillPath);
    })
    .sort();
}

/**
 * Recursively list all skill directory paths under skillsDir (relative paths).
 * Matches generate_index.py behavior so catalog includes nested skills (e.g. game-development/2d-games).
 */
function listSkillIdsRecursive(skillsDir, baseDir = skillsDir, acc = []) {
  const entries = fs.readdirSync(baseDir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    if (!entry.isDirectory()) continue;
    const dirPath = path.join(baseDir, entry.name);
    const skillPath = path.join(dirPath, 'SKILL.md');
    const relPath = path.relative(skillsDir, dirPath);
    if (fs.existsSync(skillPath)) {
      acc.push(relPath);
    }
    listSkillIdsRecursive(skillsDir, dirPath, acc);
  }
  return acc.sort();
}

module.exports = {
  listSkillIds,
  listSkillIdsRecursive,
  parseFrontmatter,
  parseInlineList,
  readSkill,
  stripQuotes,
  tokenize,
  unique,
};
