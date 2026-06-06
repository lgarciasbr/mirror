---
name: "mm-explore"
description: Activates Explorer Mode for a journey and loads exploratory context
user-invocable: true
---

# Explorer Mode

Activates Explorer Mode for a specific journey. Explorer Mode is a Mirror-native
lens for uncertainty before construction.

Explorer Mode is experimental right now. The full Explorer experience is being
built and will be available soon.

## Usage

Pi and Gemini CLI:

```text
/mm-explore <journey-slug>
```

Codex:

```text
$mm-explore <journey-slug>
```

Claude Code:

```text
/mm:explore <journey-slug>
```

Natural-language equivalents should be treated as the product interface:

```text
entrar em modo explorador nesta jornada
abrir exploração em <journey-slug>
```

## 1. Activate Explorer Mode

```bash
uv run python -m memory explore load <slug>
```

The command:

- activates `△ Explorer Mode` for the journey;
- renders the Mode Transition Surface (`△ EXPLORER MODE ACTIVE`);
- sets the journey as sticky context;
- loads Mirror identity and journey context;
- prints Explorer Mode guidance, including the experimental availability note.

## 1.1 Transition Surface

The `explore load` output includes the conversational transition surface. Render
that surface visibly to the user before continuing with exploratory work. Do not
recreate it from scratch unless the command failed to render it; copy the
rendered surface from the command output.

## 2. Work In Explorer Mode

Explorer Mode is experimental. The full Explorer experience is being built and
will be available soon.

Explorer preserves uncertainty. Builder executes commitment.

While Explorer Mode is active:

- Treat new substantive material as part of the exploratory field unless the user asks for a clear operational action.
- Preserve signals, tensions, hypotheses, corrections, and emerging story shape.
- Render `Story Thickened` when new material changes the accumulated story.
- Keep nearby signals in radar when the user asks to preserve them without opening construction.
- Do not promote to Builder or Delivery without explicit user confirmation.

## 3. Deactivation

The user should use natural language:

```text
sair do modo explorador
voltar ao modo normal
```

Mirror may then call the internal operation:

```bash
uv run python -m memory mode deactivate
```

Deactivation leaves the explicit Explorer lens and returns to Mirror Mode when
journey context remains active. Rendering and clearing the status bar are
internal effects, not user-facing operations.
