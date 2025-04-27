# Copyright (c) 2025 Osyah
# SPDX-License-Identifier: MIT

from __future__ import annotations

__all__: typing.Sequence[str] = (
    "post_content_validator",
    "channel_name_validator",
    "message_content_validator",
    "event_type_octet_validator",
    "len_eq",
    "dapp_hash_converter",
    "dapp_auth_header_converter",
    "dapp_event_body_converter",
    "uuid_converter",
)

import typing
import datetime as dt
from uuid import UUID

from attrs.validators import (
    in_,
    min_len,
    max_len,
)

from pletyvo.protocol import dapp
from pletyvo.utils import uuid7

if typing.TYPE_CHECKING:
    from pletyvo.types import UUIDLike


post_content_validator = min_len(1), max_len(2048)

channel_name_validator = min_len(1), max_len(40)

message_content_validator = min_len(1), max_len(2048)

event_type_octet_validator = in_(range(0, 256))


def len_eq(s: int):
    return min_len(s), max_len(s)


def dapp_hash_converter(h: dapp.Hash | str) -> dapp.Hash:
    if isinstance(h, str):
        return dapp.Hash.from_str(h)
    return h


def dapp_auth_header_converter(
    d: dapp.AuthHeader | dict[str, typing.Any],
) -> dapp.AuthHeader:
    if isinstance(d, dict):
        return dapp.AuthHeader.from_dict(d)
    return d


def dapp_event_body_converter(
    b: dapp.EventBody | str | bytes | bytearray,
) -> dapp.EventBody:
    if isinstance(b, str):
        return dapp.EventBody.from_str(b)
    elif isinstance(b, bytes):
        return dapp.EventBody.from_bytes(b)
    elif isinstance(b, bytearray):
        return dapp.EventBody.from_bytearray(b)
    elif isinstance(b, memoryview):
        return dapp_event_body_converter(b.tobytes())
    return b


def uuid_converter(u: UUIDLike | dt.datetime) -> UUID:
    if isinstance(u, UUID):
        return u
    elif isinstance(u, str):
        return UUID(u)
    elif isinstance(u, dt.datetime):
        return uuid7(timestamp=u.timestamp())
