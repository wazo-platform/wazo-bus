# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict

from ..common.types import Format


class DestinationConferenceDict(TypedDict, total=False):
    conference_id: int


class DestinationMeetingDict(TypedDict, total=False):
    meeting_uuid: Annotated[str, Format('uuid')]
    meeting_name: str


class DestinationUserDict(TypedDict, total=False):
    user_uuid: Annotated[str, Format('uuid')]
    user_name: str


class DestinationUnknownDict(TypedDict, total=False):
    ...


class DestinationDetailsDict(TypedDict, total=False):
    conference: DestinationConferenceDict
    meeting: DestinationMeetingDict
    user: DestinationUserDict
    unknown: DestinationUnknownDict


class RecordingDict(TypedDict, total=False):
    uuid: Annotated[str, Format('uuid')]
    start_time: str
    end_time: str
    deleted: bool
    filename: str


class CDRDataDict(TypedDict, total=False):
    id: int
    tenant_uuid: Annotated[str, Format('uuid')]
    start: Annotated[str, Format('date-time')]
    end: Annotated[str, Format('date-time')]
    answered: bool
    duration: float
    call_drection: str
    destination_details: DestinationDetailsDict
    destination_extension: str
    destination_internal_context: str
    destination_internal_extension: str
    destination_line_id: int
    destination_name: str
    destination_user_uuid: Annotated[str, Format('uuid')]
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
    source_user_uuid: Annotated[str, Format('uuid')]
    tags: list[str]
    recordings: list[RecordingDict]
