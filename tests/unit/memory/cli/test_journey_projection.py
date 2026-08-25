from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from memory.cli.journey_projection import cmd_journey_projection


def test_capabilities_returns_only_implemented_operations(capsys) -> None:
    assert (
        cmd_journey_projection(["capabilities", "--mirror-home", "/unused", "--format", "json"])
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "contractId": "mirror.journey-projections",
        "contractVersion": "1.0",
        "extensionApiVersion": "1.1",
        "operations": ["capabilities"],
    }


def test_unknown_operation_and_format_are_bounded_json(capsys) -> None:
    assert cmd_journey_projection(["not-real", "--format", "json"]) != 0
    unknown = json.loads(capsys.readouterr().out)
    assert unknown["code"] == "unsupported_contract"
    assert "not-real" not in unknown["message"]

    assert cmd_journey_projection(["capabilities", "--format", "yaml"]) != 0
    unsupported = json.loads(capsys.readouterr().out)
    assert unsupported["code"] == "unsupported_contract"
    assert "yaml" not in unsupported["message"]


def test_front_door_capabilities_uses_no_database_and_emits_one_json_document(
    tmp_path: Path,
) -> None:
    home = tmp_path / "mirror"
    env = os.environ.copy()
    env.update({"HOME": str(tmp_path), "MIRROR_HOME": str(home), "MEMORY_ENV": "test"})
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "memory",
            "journey-projection",
            "capabilities",
            "--mirror-home",
            str(home),
            "--format",
            "json",
        ],
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["contractVersion"] == "1.0"
    assert not home.exists()
    assert result.stderr == ""
