# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class DestinationConferenceDict(TypedDict):
    conference_id: int


class DestinationMeetingDict(TypedDict):
    meeting_uuid: str
    meeting_name: str


class DestinationUserDict(TypedDict):
    user_uuid: str
    user_name: str


class DestinationUnknownDict(TypedDict):
    ...


class DestinationDetailsDict(TypedDict):
    conference: DestinationConferenceDict
    meeting: DestinationMeetingDict
    user: DestinationUserDict
    unknown: DestinationUnknownDict


class RecordingDict(TypedDict):
    uuid: str
    start_time: str
    end_time: str
    deleted: bool
    filename: str


class CDRDataDict(TypedDict):
    id: int
    tenant_uuid: str
    start: str
    end: str
    answered: bool
    duration: float
    call_drection: str
    destination_details: DestinationDetailsDict
    destination_extension: str
    destination_internal_context: str
    destination_internal_extension: str
    destination_line_id: int
    destination_name: str
    destination_user_uuid: str
    requested_name: str
    requested_context: str
    requested_extension: str
    requested_internal_context: str
    requested_internal_extension: str
    source_extension: str
    source_internal_context: str
    source_internal_name: str
    source_internal_extension: str
    source_line_id: int
    source_name: str
    source_user_uuid: str
    tags: list[str]
    recordings: list[RecordingDict]
