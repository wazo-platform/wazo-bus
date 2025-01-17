# Copyright 2023-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict

from ..common.types import DateTimeStr, UUIDStr


class ApplicationCallDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_number: str
    conversation_id: str
    creation_time: DateTimeStr
    status: str
    on_hold: bool
    is_caller: bool
    dialed_extension: str
    variables: dict[str, str]
    node_uuid: UUIDStr
    moh_uuid: UUIDStr
    muted: bool
    snoops: dict[str, str]
    user_uuid: UUIDStr
    tenant_uuid: UUIDStr


class ApplicationCallPlayDict(TypedDict, total=False):
    uuid: UUIDStr
    uri: str
    language: str


class ApplicationNodeCallDict(TypedDict, total=False):
    id: str


class ApplicationNodeDict(TypedDict, total=False):
    uuid: UUIDStr
    calls: list[ApplicationNodeCallDict]


class ApplicationSnoopDict(TypedDict, total=False):
    uuid: UUIDStr
    snooped_call_id: str
    snooping_call_id: str


class CallDict(TypedDict, total=False):
    bridges: list[str]
    call_id: str
    caller_id_name: str
    caller_id_number: str
    conversation_id: str
    peer_caller_id_name: str
    peer_caller_id_number: str
    creation_time: str
    status: str
    on_hold: bool
    muted: bool
    record_state: str
    talking_to: dict[str, str]
    user_uuid: UUIDStr
    is_caller: bool
    is_video: bool
    dialed_extension: str
    line_id: int
    answer_time: str
    hangup_time: str
    direction: str


class ParkedCallDict(TypedDict, total=False):
    parking_id: int
    call_id: str
    conversation_id: str
    caller_id_name: str
    caller_id_num: str
    parker_caller_id_name: str
    parker_caller_id_num: str
    slot: str
    parked_at: DateTimeStr
    timeout_at: DateTimeStr | None


class UnparkedCallDict(ParkedCallDict, total=False):
    retriever_call_id: str
    retriever_caller_id_name: str
    retriever_caller_id_num: str


class ParkedCallTimedOutDict(ParkedCallDict, total=False):
    dialed_extension: str


class RelocateDict(TypedDict, total=False):
    uuid: UUIDStr
    relocated_call: str
    initiator_call: str
    recipient_call: str
    completions: list[str]
    initiator: str
    timeout: int
    auto_answer: bool


class TransferDict(TypedDict, total=False):
    id: str
    initiator_uuid: UUIDStr
    initiator_tenant_uuid: UUIDStr
    transferred_call: str
    initiator_call: str
    recipient_call: str
    status: str
    flow: str


class CallRecordingDict(TypedDict, total=False):
    call_id: str
