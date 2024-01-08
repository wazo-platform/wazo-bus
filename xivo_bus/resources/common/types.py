# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Annotated, Literal

_string_formats = Literal['date', 'date-time', 'uuid']


@dataclass(frozen=True)
class Format:
    format: _string_formats | None = field(default=None)


# Type aliases
UUIDStr = Annotated[str, Format('uuid')]
DateTimeStr = Annotated[str, Format('date-time')]
DateStr = Annotated[str, Format('date')]
