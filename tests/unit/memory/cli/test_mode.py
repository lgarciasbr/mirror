"""Tests for the operating mode CLI."""

from memory.cli.mode import main
from memory.config import default_db_path_for_home


def test_mode_activate_status_and_deactivate(tmp_path, capsys):
    home = tmp_path / ".mirror" / "alisson-vale"
    default_db_path_for_home(home).parent.mkdir(parents=True, exist_ok=True)

    main(["--mirror-home", str(home), "activate", "Builder Mode", "--journey", "explorer-mode"])
    assert capsys.readouterr().out.strip() == "Activated Builder Mode for explorer-mode"

    main(["--mirror-home", str(home), "status"])
    assert capsys.readouterr().out.strip() == "Builder Mode · explorer-mode"

    main(["--mirror-home", str(home), "deactivate"])
    assert capsys.readouterr().out.strip() == "Deactivated active mode"

    main(["--mirror-home", str(home), "status"])
    assert capsys.readouterr().out.strip() == "Mirror Mode"
