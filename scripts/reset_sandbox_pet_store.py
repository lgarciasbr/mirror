#!/usr/bin/env python3
"""Reset the sandbox-pet-store Builder runtime fixture.

Default state is `ariad-ready`: the journey keeps Ariad adopted, templates
prepared, and an initial cursor with no active item. Use `--state clean` to
clear Builder runtime state and remove Ariad-generated template files.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from memory import MemoryClient
from memory.builder.ariad_method import get_ariad_method
from memory.builder.delivery_cursor import clear_delivery_cursor, set_delivery_cursor
from memory.builder.method_adoption import clear_adopted_method, set_adopted_method
from memory.builder.template_generation import prepare_method_templates

JOURNEY = "sandbox-pet-store"
PROJECT_PATH = Path("/Users/alissonvale/Code/sandbox-pet-store")
ROADMAP_INDEX = PROJECT_PATH / "docs/project/roadmap/index.md"
GENERATED_FILES = (
    PROJECT_PATH / "docs/project/roadmap/ariad-adoption.md",
    PROJECT_PATH / "docs/project/roadmap/technical-debt-ledger.md",
)
GENERATED_DIRS = (PROJECT_PATH / "docs/project/roadmap/templates",)

ROADMAP_BASELINE = """# Roadmap

The roadmap describes meaningful progress for Sandbox Pet Store using current Ariad delivery language.

## Taxonomy

- **Capability Value, CV**: a major user-visible or operator-visible capability.
- **Delivery Story, DS**: a coherent delivery slice inside a CV.
- **User Story, US**: user-visible behavior that can be verified end to end.
- **Technical Story, TS**: technical substrate needed for delivery.
- **Task**: implementation step inside a User Story or Technical Story.

Legacy `CVx.Ex.Sy` references in older notes are compatibility artifacts only. New simulation work should use CV / DS / US / TS language.

## Simulation Baseline

`CV1 Cart Flow` is complete.

No Delivery Story is active at reset. Checkout is a candidate future capability, not an automatic next story. When the fixture is loaded, the Driver should orient and ask what mode the Navigator wants:

- runtime inspection;
- Delivery planning;
- Exploration.

## Capability Values

| Code | Capability Value | Status |
|------|------------------|--------|
| CV1 | Cart Flow | Done |
| CV2 | Checkout Flow | Candidate |
| CV3 | Store Polish | Future |

## CV1: Cart Flow

**Status:** Done

Purpose: make the first product movement concrete enough for a customer to start shopping.

### DS1: Basic Cart Behavior

**Status:** Done

| Code | User Story | Status | Notes |
|------|------------|--------|-------|
| US1 | Add item to cart | Done | Shows one featured product and lets the customer add it to the cart with quantity 1. |
| US2 | Update quantity | Done | Lets the customer increase and decrease quantity while keeping a minimum of 1. |
| US3 | Remove item from cart | Done | Lets the customer explicitly remove the item and return to the empty cart state. |

### DS2: Cart Review

**Status:** Done

| Code | User Story | Status | Notes |
|------|------------|--------|-------|
| US1 | Show cart summary | Done | Shows item count, subtotal, and cart total when the cart has an item. |
| US2 | Continue shopping | Done | Lets the user return to the product area while preserving cart state. |

## CV2: Checkout Flow

**Status:** Candidate

Purpose: extend the cart into a simple checkout path if the Navigator chooses Delivery work.

Candidate Delivery Stories:

- DS1 Checkout entry and address capture.
- DS2 Payment placeholder.
- DS3 Order confirmation placeholder.

These are candidates only. Do not start them automatically when the project is loaded.

## CV3: Store Polish

**Status:** Future

Potential future work:

- simple catalog filtering;
- personalization by pet profile;
- responsive layout;
- order confirmation polish.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Reset sandbox-pet-store Builder fixture")
    parser.add_argument(
        "--state",
        choices=("clean", "ariad-ready"),
        default="ariad-ready",
        help="Reset target state. Default: ariad-ready",
    )
    args = parser.parse_args()

    mem = MemoryClient()
    journey_content = mem.get_identity("journey", JOURNEY)
    if not journey_content:
        raise SystemExit(f"journey '{JOURNEY}' not found in Mirror memory")
    if not PROJECT_PATH.is_dir():
        raise SystemExit(f"project path does not exist: {PROJECT_PATH}")

    mem.journeys.set_project_path(JOURNEY, str(PROJECT_PATH))
    _restore_roadmap_baseline()
    _remove_generated_ariad_files()
    clear_adopted_method(mem.store, JOURNEY)
    clear_delivery_cursor(mem.store, JOURNEY)

    if args.state == "ariad-ready":
        set_adopted_method(mem.store, JOURNEY, "ariad")
        prepare_method_templates(PROJECT_PATH, journey=JOURNEY, method=get_ariad_method())
        set_delivery_cursor(
            mem.store,
            journey=JOURNEY,
            method="ariad",
            active_item=None,
            active_checkpoint=None,
            pending_confirmation=None,
            last_delivery_event="template_preparation",
        )

    print(f"sandbox-pet-store reset complete: state={args.state}")
    print(f"project_path={PROJECT_PATH}")
    if args.state == "ariad-ready":
        print("adopted_method=ariad")
        print("active_item=none")
        print("last_delivery_event=template_preparation")


def _restore_roadmap_baseline() -> None:
    ROADMAP_INDEX.parent.mkdir(parents=True, exist_ok=True)
    ROADMAP_INDEX.write_text(ROADMAP_BASELINE, encoding="utf-8")


def _remove_generated_ariad_files() -> None:
    for path in GENERATED_FILES:
        path.unlink(missing_ok=True)
    for path in GENERATED_DIRS:
        if path.exists():
            shutil.rmtree(path)


if __name__ == "__main__":
    main()
