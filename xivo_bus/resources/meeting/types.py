# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated, TypedDict

from ..common.types import Format


class MeetingDict(TypedDict, total=False):
    uuid: Annotated[str, Format('uuid')]
    name: str
    owner_uuids: Annotated[list[str], Format('uuid')]
    ingress_http_uri: str
    guest_sip_authorization: str | None  # b64 encoded


class MeetingAuthorizationDict(TypedDict, total=False):
    uuid: Annotated[str, Format('uuid')]
    meeting_uuid: Annotated[str, Format('uuid')]
    guest_uuid: Annotated[str, Format('uuid')]
    guest_name: str
    status: str
    creation_time: str


class MeetingParticipantDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_number: str
    call_id: str
    user_uuid: Annotated[str | None, Format('uuid')]
