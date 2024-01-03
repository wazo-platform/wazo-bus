# Copyright 2023-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class ApplicationCallDict(TypedDict, total=False):
    id: str
    caller_id_name: str
    caller_id_number: str
    creation_time: str
    status: str
    on_hold: bool
    is_caller: bool
    dialed_extension: str
    variables: dict[str, str]
    node_uuid: str
    moh_uuid: str
    muted: bool
    snoops: dict[str, str]
    user_uuid: str
    tenant_uuid: str


class ApplicationCallPlayDict(TypedDict, total=False):
    uuid: str
    uri: str
    language: str


class ApplicationNodeCallDict(TypedDict, total=False):
    id: str


class ApplicationNodeDict(TypedDict, total=False):
    uuid: str
    calls: list[ApplicationNodeCallDict]


class ApplicationSnoopDict(TypedDict, total=False):
    uuid: str
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
    user_uuid: str
    is_caller: bool
    is_video: bool
    dialed_extension: str
    line_id: int
    answer_time: str
    hangup_time: str
    direction: str


class RelocateDict(TypedDict, total=False):
    uuid: str
    relocated_call: str
    initiator_call: str
    recipient_call: str
    completions: list[str]
    initiator: str
    timeout: int
    auto_answer: bool


class TransferDict(TypedDict, total=False):
    id: str
    initiator_uuid: str
    initiator_tenant_uuid: str
    transferred_call: str
    initiator_call: str
    recipient_call: str
    status: str
    flow: str