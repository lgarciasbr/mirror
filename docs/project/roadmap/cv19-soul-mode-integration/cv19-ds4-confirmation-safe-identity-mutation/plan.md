[< Story](index.md)

# Plan — CV19.DS4 Confirmation And Safe Identity Mutation

## Boundary

Only confirmed proposals mutate identity. Confirmation must be explicit and visible.

## Design

Command:

```bash
uv run python -m memory soul apply self \
  --proposed "exact content to write" \
  --confirm APPLY
```

Defaults:

- `self` → `soul`
- `shadow` → `profile`
- `ego` → `behavior`
- `persona` → requires `--key`

The command uses `MemoryClient.set_identity()` and renders an identity-updated surface. Because this writes the exact target content, the assistant must confirm that the proposed text is the intended full target content or explicit additive section before applying. Do not overwrite a longer identity document with a short fragment unless that is explicitly the approved replacement.

## Validation

- Missing `--confirm APPLY` exits without mutation.
- Confirmed apply writes identity.
- Apply uses the exact approved content, not a paraphrase.
- Unsupported/missing keys fail safely.
