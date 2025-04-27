# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = ("Engine",)

import typing
from abc import (
    ABC,
    abstractmethod,
)

if typing.TYPE_CHECKING:
    from pletyvo.types import JSONType


class Engine(ABC):
    @abstractmethod
    async def get(self, endpoint: str) -> JSONType: ...

    @abstractmethod
    async def post(self, endpoint: str, body: JSONType) -> JSONType: ...
