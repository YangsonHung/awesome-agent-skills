# Novel Writer

A Claude Code skill for novel writing, providing professional support from ideation, planning, writing, to revision.

## Features

- **Create New Novel** - Start from scratch with structured outline guidance
- **Continue Chapters** - Write new chapters based on existing content
- **Character Design** - Create deep characters with desires, fears, and arcs
- **Worldbuilding** - Build complete story worlds

## Supported Genres

- Science Fiction
- Fantasy
- Mystery/Thriller
- Romance
- Historical/Wuxia
- Horror/Thriller

## Installation

Copy this skill to your Claude Code skills directory:

```bash
cp -r . ~/.claude/skills/novel-writer
```

Or download the `.skill` file and import it.

## Usage

After installation, Claude will automatically recognize these requests:

- "help me write a sci-fi novel"
- "write the next chapter"
- "design a villain character"
- "build a magic system"

## Structure

```
novel-writer/
├── SKILL.md                      # Core guidance file
├── references/                   # Reference documentation
│   ├── story-structure.md        # Story structure (Three-Act, Hero's Journey, etc.)
│   ├── character-development.md  # Character development (archetypes, dimensions, arcs)
│   ├── worldbuilding.md          # Worldbuilding guide
│   ├── writing-techniques.md     # Writing techniques (POV, scenes, dialogue, etc.)
│   └── genre-guides.md           # Genre-specific guides
└── assets/templates/             # Template files
    ├── outline.md                # Novel outline template
    ├── character-card.md         # Character card template
    ├── world-bible.md            # Worldbuilding template
    └── chapter.md                # Chapter planning template
```

## License

MIT
