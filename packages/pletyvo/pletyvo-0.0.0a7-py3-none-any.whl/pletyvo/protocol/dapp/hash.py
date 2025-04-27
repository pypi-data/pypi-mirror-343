# Copyright (c) 2024-2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "HASH_SIZE",
    "HASH_LENGTH",
    "Hash",
)

import base64
import typing

import attrs
from blake3 import blake3

from pletyvo.utils import padd
from pletyvo.codec.sanitizer import len_eq


HASH_SIZE: typing.Final[int] = 32
HASH_LENGTH: typing.Final[int] = 43


@attrs.define(hash=True)
class Hash:
    data: bytes = attrs.field(validator=len_eq(HASH_SIZE))

    def __str__(self) -> str:
        return base64.urlsafe_b64encode(bytes(self)).decode("utf-8").rstrip("=")

    def __len__(self) -> int:
        return len(str(self))

    def __bytes__(self) -> bytes:
        return self.data

    @classmethod
    def from_str(cls, s: str) -> Hash:
        if len(s) != HASH_LENGTH:
            error_message = f"Hash must have {HASH_LENGTH} characters, not {len(s)}"
            raise ValueError(error_message)
        return cls(base64.urlsafe_b64decode(padd(s)))

    @classmethod
    def gen(cls, sch: int, data: bytes) -> Hash:
        data = bytes((sch,)) + data
        data = blake3(data).digest(length=32)
        return cls(data)
