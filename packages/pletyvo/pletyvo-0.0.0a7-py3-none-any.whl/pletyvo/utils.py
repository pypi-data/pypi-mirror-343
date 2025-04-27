# Copyright (c) 2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "padd",
    "uuid7",
)

import typing

import uuid
import uuid_utils


def padd(s: str) -> str:
    return s + "=" * (-len(s) % 4)


def uuid7(
    timestamp: typing.Optional[float] = None,
) -> uuid.UUID:
    if timestamp:
        t, n = divmod(timestamp, 1)
        t, n = round(t), round((n % 1) * 1_000_000_000)
        return uuid.UUID(int=uuid_utils.uuid7(t, n).int)
    return uuid.UUID(int=uuid_utils.uuid7().int)
