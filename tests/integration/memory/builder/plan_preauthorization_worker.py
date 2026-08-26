from __future__ import annotations

import argparse
import json
from pathlib import Path

from memory import MemoryClient
from memory.builder.delivery_story_plan import approve_delivery_story_plan


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--result", required=True, type=Path)
    args = parser.parse_args()

    client = MemoryClient(env="test", db_path=args.db)
    client.store.configure_projection_refresh(None)
    report = approve_delivery_story_plan(
        client.store,
        journey="sandbox-pet-store",
        method="ariad",
        plan_artifact_path=args.plan,
        use_preauthorization=True,
    )
    args.result.write_text(
        json.dumps(
            {
                "status": report.status,
                "implementationStarted": report.implementation_started,
            },
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
