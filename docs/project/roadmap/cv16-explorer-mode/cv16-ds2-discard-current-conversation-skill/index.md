[< CV16](../index.md)

# CV16.DS2 — Discard Current Conversation Skill

**Status:** ✅ Done  
**Placement:** CV16 runtime hygiene support  
**User-visible outcome:** The user can leave a test session while deleting the current conversation from the Mirror database, preventing exploratory/runtime smoke tests from polluting conversation history.

---

## Why This Exists

Mode and transition-surface work requires frequent manual testing in the real
Mirror runtime. Those tests create conversations that are operationally useful in
the moment but should not become durable memory or conversation history.

The user needs a safe exit path:

```text
sair descartando esta conversa
quit and discard this conversation
```

This is not normal deletion from the web console. It is a runtime hygiene action
for the active session.

---

## Scope

- Add a CLI operation to discard the current runtime conversation.
- Resolve the current conversation from an explicit session id when available, or
  from the latest active Pi session for the Pi skill path.
- Delete messages, conversation embeddings, conversation row, and detach any
  dependent references using the existing conversation deletion service.
- Mark the runtime session so the assistant response confirming the discard does
  not recreate a new conversation immediately.
- Add a Pi skill that runs the discard operation and tells the user to exit Pi.

---

## Non-goals

- No automatic terminal quit from Python core.
- No bulk cleanup.
- No deletion of extracted memories beyond detaching their conversation id, matching existing conversation deletion semantics.
- No web UI changes.

---

## Acceptance Behavior

Given a Pi session has a current conversation, when the discard-current operation
runs, then the conversation and its messages are removed from the database and
the runtime session no longer points at that conversation.

Given the discard operation runs during a skill response, when Pi logs the
assistant's confirmation turn, then the logger skips that assistant message so a
new conversation is not immediately created.

Given the next user prompt happens in the same runtime session instead of the
user quitting, then the discard marker is cleared and normal logging can create a
new conversation.

---

## References

- [Plan](plan.md)
- [Test Guide](test-guide.md)
