# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

string_formats = Literal['date', 'date-time', 'uuid']


@dataclass
class Metadata:
    format: string_formats | None = field(default=None)


@dataclass
class Format:
    format: string_formats | None = field(default=None)
