# Project Mjölnir

Project Mjölnir is a modular, cross-platform parser and database builder for D&D 3.5e sourcebooks and indexes.

It automatically ingests `.docx` indexes for:
- Deities
- Feats
- Spells
- Mundane Items
- Magic Items
- Races
- Classes (Base + Prestige)
- Monsters (NPCs included)
- Templates

Parsed data is inserted into a clean SQLite database according to a relational schema.

Mjolnir includes:
- Modular parser system (one parser per entity type)
- Smart file type detection
- Text cleaning utilities
- Full logging and troubleshooting output
- Open structure for future VTT support and PC/NPC generators

**Mjolnir is designed to forge your D&D 3.5 source material into true power.**

## Usage

```bash
python mjolnir.py path_to_folder_or_file
```

Files are detected, parsed, and loaded into the database automatically.

.docx format required.