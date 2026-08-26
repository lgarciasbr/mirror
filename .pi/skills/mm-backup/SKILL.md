---
name: "mm-backup"
description: Backs up the production memory database and mirrors the backup into Obsidian
user-invocable: true
---

# Backup

When receiving `/mm-backup`, create the canonical Mirror backup first, then copy
the resulting artifact into the Obsidian backup folder.

## Canonical destination

Always preserve Mirror's default backup location as the source of truth:

```text
~/.mirror-minds/leandro/backups/
```

Run:

```bash
uv run python -m memory backup
```

## Obsidian copy

After the canonical backup succeeds, copy the newest `memory_*.zip` from the
default backup directory into:

```text
/Users/leandro/Library/CloudStorage/OneDrive-i9Flow/Documentos - Geral/Projetos/Leandro/Backups/Mirror Mind/
```

Also keep/update the folder's `README.md` with the timestamp and latest copied
backup filename.

## Ariad companion backup

When the user asks for Mirror + Ariad backup, also create a separate Ariad zip
from the Mirror repository containing Ariad-related docs, code, skills, and
tests, then copy it into the same Obsidian folder with its manifest:

```bash
cd /Users/leandro/Documents/Código/mirror
ts=$(date -u +%Y%m%dT%H%M%SZ)
out="/tmp/ariad_backup_${ts}.zip"
manifest="/tmp/ariad_backup_${ts}_manifest.txt"
{
  find docs src tests .pi -type f 2>/dev/null | grep -i ariad || true
  find docs/project/roadmap -type f -path '*cv20-builder-mode-evolution*' 2>/dev/null || true
} | sort -u > "$manifest"
zip -q "$out" -@ < "$manifest"
```

Copy both `$out` and `$manifest` into the Obsidian backup folder.

## Validation

Validate every copied zip:

```bash
unzip -tq "path/to/archive.zip"
```

Report both locations to the user: the canonical Mirror backup path and the
Obsidian copy path. If the Obsidian folder cannot be found, do not skip silently;
ask where to copy it.
