# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class RecordingsAnnouncementsDict(TypedDict):
    recording_start: str | None
    recording_stop: str | None
