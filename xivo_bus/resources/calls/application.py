# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Any

from xivo_bus.resources.common.event import TenantEvent, UserEvent

from .types import (
    ApplicationCallDict,
    ApplicationCallPlayDict,
    ApplicationNodeDict,
    ApplicationSnoopDict,
)


class _ApplicationMixin:
    def __init__(self, content: dict, application_uuid: str, *args: Any):
        super().__init__(content, *args)  # type: ignore[call-arg]
        if application_uuid is None:
            raise ValueError('application_uuid must have a value')
        self.application_uuid = str(application_uuid)


class ApplicationCallDTMFReceivedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_call_dtmf_received'
    routing_key_fmt = 'applications.{application_uuid}.calls.{call_id}.dtmf.created'

    def __init__(
        self, call_id: str, dtmf: str, application_uuid: str, tenant_uuid: str
    ):
        content = {
            'application_uuid': str(application_uuid),
            'call_id': call_id,
            'dtmf': dtmf,
        }
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationCallEnteredEvent(_ApplicationMixin, UserEvent):
    service = 'calld'
    name = 'application_call_entered'
    routing_key_fmt = 'applications.{application_uuid}.calls.created'

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: str,
        tenant_uuid: str,
        user_uuid: str,
    ):
        content = {'application_uuid': str(application_uuid), 'call': application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallInitiatedEvent(_ApplicationMixin, UserEvent):
    service = 'calld'
    name = 'application_call_initiated'
    routing_key_fmt = 'applications.{application_uuid}.calls.created'

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: str,
        tenant_uuid: str,
        user_uuid: str,
    ):
        content = {'application_uuid': str(application_uuid), 'call': application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallDeletedEvent(_ApplicationMixin, UserEvent):
    service = 'calld'
    name = 'application_call_deleted'
    routing_key_fmt = 'applications.{application_uuid}.calls.{call[id]}.deleted'

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: str,
        tenant_uuid: str,
        user_uuid: str,
    ):
        content = {'application_uuid': str(application_uuid), 'call': application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallUpdatedEvent(_ApplicationMixin, UserEvent):
    service = 'calld'
    name = 'application_call_updated'
    routing_key_fmt = 'applications.{application_uuid}.calls.{call[id]}.updated'

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: str,
        tenant_uuid: str,
        user_uuid: str,
    ):
        content = {'application_uuid': str(application_uuid), 'call': application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallAnsweredEvent(_ApplicationMixin, UserEvent):
    service = 'calld'
    name = 'application_call_answered'
    routing_key_fmt = 'applications.{application_uuid}.calls.{call[id]}.answered'

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: str,
        tenant_uuid: str,
        user_uuid: str,
    ):
        content = {'application_uuid': str(application_uuid), 'call': application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallProgressStartedEvent(_ApplicationMixin, UserEvent):
    service = 'calld'
    name = 'application_progress_started'
    routing_key_fmt = (
        'applications.{application_uuid}.calls.{call[id]}.progress.started'
    )

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: str,
        tenant_uuid: str,
        user_uuid: str,
    ):
        content = {'application_uuid': str(application_uuid), 'call': application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationCallProgressStoppedEvent(_ApplicationMixin, UserEvent):
    service = 'calld'
    name = 'application_progress_stopped'
    routing_key_fmt = (
        'applications.{application_uuid}.calls.{call[id]}.progress.stopped'
    )

    def __init__(
        self,
        application_call: ApplicationCallDict,
        application_uuid: str,
        tenant_uuid: str,
        user_uuid: str,
    ):
        content = {'application_uuid': str(application_uuid), 'call': application_call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)


class ApplicationDestinationNodeCreatedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_destination_node_created'
    routing_key_fmt = 'applications.{application_uuid}.nodes.created'

    def __init__(
        self, node: ApplicationNodeDict, application_uuid: str, tenant_uuid: str
    ):
        content = {'application_uuid': str(application_uuid), 'node': node}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationNodeCreatedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_node_created'
    routing_key_fmt = 'applications.{application_uuid}.nodes.created'

    def __init__(
        self, node: ApplicationNodeDict, application_uuid: str, tenant_uuid: str
    ):
        content = {'application_uuid': str(application_uuid), 'node': node}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationNodeUpdatedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_node_updated'
    routing_key_fmt = 'applications.{application_uuid}.nodes.{node[uuid]}.updated'

    def __init__(
        self, node: ApplicationNodeDict, application_uuid: str, tenant_uuid: str
    ):
        content = {'application_uuid': str(application_uuid), 'node': node}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationNodeDeletedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_node_deleted'
    routing_key_fmt = 'applications.{application_uuid}.nodes.{node[uuid]}.deleted'

    def __init__(
        self, node: ApplicationNodeDict, application_uuid: str, tenant_uuid: str
    ):
        content = {'application_uuid': str(application_uuid), 'node': node}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationPlaybackCreatedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_playback_created'
    routing_key_fmt = (
        'applications.{application_uuid}.playbacks.{playback[uuid]}.created'
    )

    def __init__(
        self, playback: ApplicationCallPlayDict, application_uuid: str, tenant_uuid: str
    ):
        content = {
            'application_uuid': str(application_uuid),
            'playback': playback,
        }
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationPlaybackDeletedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_playback_deleted'
    routing_key_fmt = (
        'applications.{application_uuid}.playbacks.{playback[uuid]}.deleted'
    )

    def __init__(
        self, playback: ApplicationCallPlayDict, application_uuid: str, tenant_uuid: str
    ):
        content = {
            'application_uuid': str(application_uuid),
            'playback': playback,
        }
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationSnoopCreatedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_snoop_created'
    routing_key_fmt = 'applications.{application_uuid}.snoops.{snoop[uuid]}.created'

    def __init__(
        self, snoop: ApplicationSnoopDict, application_uuid: str, tenant_uuid: str
    ):
        content = {'application_uuid': str(application_uuid), 'snoop': snoop}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationSnoopUpdatedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_snoop_updated'
    routing_key_fmt = 'applications.{application_uuid}.snoops.{snoop[uuid]}.updated'

    def __init__(
        self, snoop: ApplicationSnoopDict, application_uuid: str, tenant_uuid: str
    ):
        content = {'application_uuid': str(application_uuid), 'snoop': snoop}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationSnoopDeletedEvent(_ApplicationMixin, TenantEvent):
    service = 'calld'
    name = 'application_snoop_deleted'
    routing_key_fmt = 'applications.{application_uuid}.snoops.{snoop[uuid]}.deleted'

    def __init__(
        self, snoop: ApplicationSnoopDict, application_uuid: str, tenant_uuid: str
    ):
        content = {'application_uuid': str(application_uuid), 'snoop': snoop}
        super().__init__(content, application_uuid, tenant_uuid)


class ApplicationUserOutgoingCallCreatedEvent(_ApplicationMixin, UserEvent):
    service = 'calld'
    name = 'application_user_outgoing_call_created'
    routing_key_fmt = (
        'applications.{application_uuid}.user_outgoing_call.{call[id]}.created'
    )

    def __init__(
        self,
        call: ApplicationCallDict,
        application_uuid: str,
        tenant_uuid: str,
        user_uuid: str,
    ):
        content = {'application_uuid': str(application_uuid), 'call': call}
        super().__init__(content, application_uuid, tenant_uuid, user_uuid)
