[< Story](index.md)

# Test Guide — CV16.DS2 Discard Current Conversation Skill

## Automated Verification

```bash
uv run pytest tests/unit/memory/cli/test_conversation_logger_discard.py
uv run ruff check src/memory/cli/conversation_logger.py tests/unit/memory/cli/test_conversation_logger_discard.py
```

Expected: all checks pass.

## Manual Validation

From a Pi session with a conversation you want to discard:

```text
/mm-discard
```

or natural language:

```text
sair descartando esta conversa
```

Expected response:

```text
Conversa atual descartada do banco. Pode sair com /quit.
```

Then quit Pi:

```text
/quit
```

Expected database behavior:

- the current conversation row is deleted;
- messages for that conversation are deleted;
- runtime session no longer points to the deleted conversation;
- the assistant confirmation turn does not create a new conversation.
