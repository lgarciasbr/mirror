from __future__ import annotations

import sys
from pathlib import Path

from memory.web.command_executor import ControlledCommand, run_controlled_command


def test_controlled_command_captures_successful_output(tmp_path: Path) -> None:
    result = run_controlled_command(
        ControlledCommand(
            id="python-echo",
            argv=(sys.executable, "-c", "print('hello')"),
            cwd=tmp_path,
        )
    )

    assert result.succeeded is True
    assert result.return_code == 0
    assert result.timed_out is False
    assert result.stdout.strip() == "hello"
    assert result.stderr == ""
    assert result.to_dict()["argv"] == [sys.executable, "-c", "print('hello')"]


def test_controlled_command_captures_nonzero_exit(tmp_path: Path) -> None:
    result = run_controlled_command(
        ControlledCommand(
            id="python-fail",
            argv=(sys.executable, "-c", "import sys; print('no'); sys.exit(7)"),
            cwd=tmp_path,
        )
    )

    assert result.succeeded is False
    assert result.return_code == 7
    assert result.stdout.strip() == "no"


def test_controlled_command_times_out(tmp_path: Path) -> None:
    result = run_controlled_command(
        ControlledCommand(
            id="python-sleep",
            argv=(sys.executable, "-c", "import time; time.sleep(2)"),
            cwd=tmp_path,
            timeout_seconds=1,
        )
    )

    assert result.succeeded is False
    assert result.return_code is None
    assert result.timed_out is True


def test_controlled_command_bounds_output(tmp_path: Path) -> None:
    result = run_controlled_command(
        ControlledCommand(
            id="python-large-output",
            argv=(sys.executable, "-c", "print('x' * 50)"),
            cwd=tmp_path,
            output_limit=10,
        )
    )

    assert result.stdout.startswith("x" * 10)
    assert "truncated" in result.stdout


def test_controlled_command_requires_existing_cwd(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    try:
        run_controlled_command(
            ControlledCommand(
                id="bad-cwd",
                argv=(sys.executable, "-c", "print('x')"),
                cwd=missing,
            )
        )
    except ValueError as exc:
        assert "existing directory" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing cwd")
