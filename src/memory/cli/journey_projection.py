"""CLI transport for Journey Projection Contract operations."""

from __future__ import annotations

import json
from collections.abc import Mapping, Sequence

from memory.journey_projections.constants import (
    CONTRACT_ID,
    CONTRACT_VERSION,
    EXTENSION_API_VERSION,
    IMPLEMENTED_OPERATIONS,
)
from memory.journey_projections.errors import ProjectionError, ProjectionErrorCode


def _emit(payload: Mapping[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def _parse_common(args: Sequence[str]) -> tuple[str | None, str, list[str]]:
    mirror_home: str | None = None
    output_format = "json"
    positional: list[str] = []
    index = 0
    while index < len(args):
        argument = args[index]
        if argument == "--mirror-home" and index + 1 < len(args):
            mirror_home = args[index + 1]
            index += 2
        elif argument == "--format" and index + 1 < len(args):
            output_format = args[index + 1]
            index += 2
        else:
            positional.append(argument)
            index += 1
    return mirror_home, output_format, positional


def _unsupported() -> ProjectionError:
    return ProjectionError(
        ProjectionErrorCode.UNSUPPORTED_CONTRACT,
        "Journey projection operation is unavailable for this contract version.",
    )


def cmd_journey_projection(args: Sequence[str]) -> int:
    _mirror_home, output_format, positional = _parse_common(args)
    if output_format != "json" or len(positional) != 1:
        _emit(_unsupported().to_dict())
        return 2

    operation = positional[0]
    if operation != "capabilities":
        _emit(_unsupported().to_dict())
        return 2

    _emit(
        {
            "contractId": CONTRACT_ID,
            "contractVersion": CONTRACT_VERSION,
            "extensionApiVersion": EXTENSION_API_VERSION,
            "operations": list(IMPLEMENTED_OPERATIONS),
        }
    )
    return 0
