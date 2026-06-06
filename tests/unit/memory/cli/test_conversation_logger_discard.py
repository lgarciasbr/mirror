"""Tests for discarding the current conversation."""

import json

from memory import MemoryClient
from memory.cli.conversation_logger import (
    discard_current_conversation,
    log_assistant_message,
    log_user_message,
)
from memory.config import default_db_path_for_home


def test_discard_current_conversation_deletes_active_session_conversation(tmp_path):
    home = tmp_path / ".mirror" / "alisson-vale"
    db_path = default_db_path_for_home(home)

    log_user_message("sess-1", "test prompt", interface="pi", mirror_home=home)
    mem = MemoryClient(db_path=db_path)
    session = mem.store.get_runtime_session("sess-1")
    assert session is not None
    conversation_id = session.conversation_id
    assert conversation_id is not None
    assert mem.store.get_conversation(conversation_id) is not None
    mem.close()

    discarded = discard_current_conversation(session_id="sess-1", mirror_home=home)

    mem = MemoryClient(db_path=db_path)
    assert discarded == conversation_id
    assert mem.store.get_conversation(conversation_id) is None
    session = mem.store.get_runtime_session("sess-1")
    assert session is not None
    assert session.conversation_id is None
    assert json.loads(session.metadata or "{}") == {"discard_current_conversation": True}


def test_discard_marker_skips_confirmation_assistant_log(tmp_path):
    home = tmp_path / ".mirror" / "alisson-vale"
    db_path = default_db_path_for_home(home)

    log_user_message("sess-1", "test prompt", interface="pi", mirror_home=home)
    discard_current_conversation(session_id="sess-1", mirror_home=home)

    log_assistant_message("sess-1", "discarded; quit now", interface="pi", mirror_home=home)

    mem = MemoryClient(db_path=db_path)
    session = mem.store.get_runtime_session("sess-1")
    assert session is not None
    assert session.conversation_id is None
    assert mem.store.conn.execute("SELECT COUNT(*) AS c FROM conversations").fetchone()["c"] == 0


def test_next_user_message_after_discard_starts_fresh_conversation(tmp_path):
    home = tmp_path / ".mirror" / "alisson-vale"
    db_path = default_db_path_for_home(home)

    log_user_message("sess-1", "test prompt", interface="pi", mirror_home=home)
    discard_current_conversation(session_id="sess-1", mirror_home=home)

    log_user_message("sess-1", "new prompt", interface="pi", mirror_home=home)

    mem = MemoryClient(db_path=db_path)
    session = mem.store.get_runtime_session("sess-1")
    assert session is not None
    assert session.conversation_id is not None
    assert session.metadata is None
    messages = mem.store.get_messages(session.conversation_id)
    assert [m.content for m in messages] == ["new prompt"]
