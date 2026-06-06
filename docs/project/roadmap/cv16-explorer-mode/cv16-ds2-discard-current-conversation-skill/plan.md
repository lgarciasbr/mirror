[< Story](index.md)

# Plan — CV16.DS2 Discard Current Conversation Skill

## Boundary

This story is a runtime hygiene action. It deletes the current conversation from
the database, but it does not force-close the terminal runtime. The skill can
only tell the user to quit after the discard.

## Implementation

- Add `conversation-logger discard-current`.
- Accept optional `--session-id`; otherwise resolve the latest active Pi session.
- Use `ConversationService.delete_conversations()` for deletion so existing
  dependency cleanup remains consistent.
- After deletion, update the runtime session with `conversation_id=NULL`,
  `active=false`, and metadata marker `discard_current_conversation=true`.
- Update `log_assistant_message()` to skip logging once when that marker is
  present.
- Update `log_user_message()` to clear the marker if the user continues in the
  same session.
- Add `.pi/skills/mm-discard/SKILL.md` as the user-facing skill.

## Validation

```bash
uv run pytest tests/unit/memory/cli/test_conversation_logger_discard.py
uv run ruff check src/memory/cli/conversation_logger.py tests/unit/memory/cli/test_conversation_logger_discard.py
```

Manual smoke:

```bash
uv run python -m memory conversation-logger discard-current --session-id <session-id>
```

Expected: current conversation is deleted and the next assistant confirmation is
not logged as a new conversation.
