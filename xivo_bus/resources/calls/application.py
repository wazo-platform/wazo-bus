# Copyright 2022-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent, UserEvent


class _ApplicationMixin(object):
    def __init__(self, content, application_uuid, *args):
        super(_ApplicationMixin, self).__init__(content, *args)
        if application_uuid is None:
            raise ValueError('application_uuid must have a value')
        self.application_uuid = str(application_uuid)


class ApplicationCallDTMFReceivedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_call_dtmf_received'
    routing_key_fmt = 'applications.{application_uuid}.calls.{call_id}.dtmf.created'

    def __init__(self, call_id, dtmf, application_uuid, tenant_uuid):
        content = {
            'application_uuid': str(application_uuid),
            'call_id': call_id,
            'dtmf': dtmf,
        }
        super(ApplicationCallDTMFReceivedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationCallEnteredEvent(_ApplicationMixin, UserEvent):
    name = 'application_call_entered'
    routing_key_fmt = 'applications.{application_uuid}.calls.created'

    def __init__(self, call_schema, application_uuid, tenant_uuid, user_uuid):
        content = {'application_uuid': str(application_uuid), 'call': call_schema}
        super(ApplicationCallEnteredEvent, self).__init__(
            content, application_uuid, tenant_uuid, user_uuid
        )


class ApplicationCallInitiatedEvent(_ApplicationMixin, UserEvent):
    name = 'application_call_initiated'
    routing_key_fmt = 'applications.{application_uuid}.calls.created'

    def __init__(self, call_schema, application_uuid, tenant_uuid, user_uuid):
        content = {'application_uuid': str(application_uuid), 'call': call_schema}
        super(ApplicationCallInitiatedEvent, self).__init__(
            content, application_uuid, tenant_uuid, user_uuid
        )


class ApplicationCallDeletedEvent(_ApplicationMixin, UserEvent):
    name = 'application_call_deleted'
    routing_key_fmt = 'applications.{application_uuid}.calls.{call[id]}.deleted'

    def __init__(self, call_schema, application_uuid, tenant_uuid, user_uuid):
        content = {'application_uuid': str(application_uuid), 'call': call_schema}
        super(ApplicationCallDeletedEvent, self).__init__(
            content, application_uuid, tenant_uuid, user_uuid
        )


class ApplicationCallUpdatedEvent(_ApplicationMixin, UserEvent):
    name = 'application_call_updated'
    routing_key_fmt = 'applications.{application_uuid}.calls.{call[id]}.updated'

    def __init__(self, call_schema, application_uuid, tenant_uuid, user_uuid):
        content = {'application_uuid': str(application_uuid), 'call': call_schema}
        super(ApplicationCallUpdatedEvent, self).__init__(
            content, application_uuid, tenant_uuid, user_uuid
        )


class ApplicationCallAnsweredEvent(_ApplicationMixin, UserEvent):
    name = 'application_call_answered'
    routing_key_fmt = 'applications.{application_uuid}.calls.{call[id]}.answered'

    def __init__(self, call_schema, application_uuid, tenant_uuid, user_uuid):
        content = {'application_uuid': str(application_uuid), 'call': call_schema}
        super(ApplicationCallAnsweredEvent, self).__init__(
            content, application_uuid, tenant_uuid, user_uuid
        )


class ApplicationCallProgressStartedEvent(_ApplicationMixin, UserEvent):
    name = 'application_progress_started'
    routing_key_fmt = (
        'applications.{application_uuid}.calls.{call[id]}.progress.started'
    )

    def __init__(self, call_schema, application_uuid, tenant_uuid, user_uuid):
        content = {'application_uuid': str(application_uuid), 'call': call_schema}
        super(ApplicationCallProgressStartedEvent, self).__init__(
            content, application_uuid, tenant_uuid, user_uuid
        )


class ApplicationCallProgressStoppedEvent(_ApplicationMixin, UserEvent):
    name = 'application_progress_stopped'
    routing_key_fmt = (
        'applications.{application_uuid}.calls.{call[id]}.progress.stopped'
    )

    def __init__(self, call_schema, application_uuid, tenant_uuid, user_uuid):
        content = {'application_uuid': str(application_uuid), 'call': call_schema}
        super(ApplicationCallProgressStoppedEvent, self).__init__(
            content, application_uuid, tenant_uuid, user_uuid
        )


class ApplicationDestinationNodeCreatedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_destination_node_created'
    routing_key_fmt = 'applications.{application_uuid}.nodes.created'

    def __init__(self, node_schema, application_uuid, tenant_uuid):
        content = {'application_uuid': str(application_uuid), 'node': node_schema}
        super(ApplicationDestinationNodeCreatedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationNodeCreatedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_node_created'
    routing_key_fmt = 'applications.{application_uuid}.nodes.created'

    def __init__(self, node_schema, application_uuid, tenant_uuid):
        content = {'application_uuid': str(application_uuid), 'node': node_schema}
        super(ApplicationNodeCreatedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationNodeUpdatedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_node_updated'
    routing_key_fmt = 'applications.{application_uuid}.nodes.{node[uuid]}.updated'

    def __init__(self, node_schema, application_uuid, tenant_uuid):
        content = {'application_uuid': str(application_uuid), 'node': node_schema}
        super(ApplicationNodeUpdatedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationNodeDeletedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_node_deleted'
    routing_key_fmt = 'applications.{application_uuid}.nodes.{node[uuid]}.deleted'

    def __init__(self, node_schema, application_uuid, tenant_uuid):
        content = {'application_uuid': str(application_uuid), 'node': node_schema}
        super(ApplicationNodeDeletedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationPlaybackCreatedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_playback_created'
    routing_key_fmt = (
        'applications.{application_uuid}.playbacks.{playback[uuid]}.created'
    )

    def __init__(self, playback_schema, application_uuid, tenant_uuid):
        content = {
            'application_uuid': str(application_uuid),
            'playback': playback_schema,
        }
        super(ApplicationPlaybackCreatedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationPlaybackDeletedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_playback_deleted'
    routing_key_fmt = (
        'applications.{application_uuid}.playbacks.{playback[uuid]}.deleted'
    )

    def __init__(self, playback_schema, application_uuid, tenant_uuid):
        content = {
            'application_uuid': str(application_uuid),
            'playback': playback_schema,
        }
        super(ApplicationPlaybackDeletedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationSnoopCreatedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_snoop_created'
    routing_key_fmt = 'applications.{application_uuid}.snoops.{snoop[uuid]}.created'

    def __init__(self, snoop_schema, application_uuid, tenant_uuid):
        content = {'application_uuid': str(application_uuid), 'snoop': snoop_schema}
        super(ApplicationSnoopCreatedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationSnoopUpdatedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_snoop_updated'
    routing_key_fmt = 'applications.{application_uuid}.snoops.{snoop[uuid]}.updated'

    def __init__(self, snoop_schema, application_uuid, tenant_uuid):
        content = {'application_uuid': str(application_uuid), 'snoop': snoop_schema}
        super(ApplicationSnoopUpdatedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationSnoopDeletedEvent(_ApplicationMixin, TenantEvent):
    name = 'application_snoop_deleted'
    routing_key_fmt = 'applications.{application_uuid}.snoops.{snoop[uuid]}.deleted'

    def __init__(self, snoop_schema, application_uuid, tenant_uuid):
        content = {'application_uuid': str(application_uuid), 'snoop': snoop_schema}
        super(ApplicationSnoopDeletedEvent, self).__init__(
            content, application_uuid, tenant_uuid
        )


class ApplicationUserOutgoingCallCreatedEvent(_ApplicationMixin, UserEvent):
    name = 'application_user_outgoing_call_created'
    routing_key_fmt = (
        'applications.{application_uuid}.user_outgoing_call.{call[id]}.created'
    )

    def __init__(self, call_schema, application_uuid, tenant_uuid, user_uuid):
        content = {'application_uuid': str(application_uuid), 'call': call_schema}
        super(ApplicationUserOutgoingCallCreatedEvent, self).__init__(
            content, application_uuid, tenant_uuid, user_uuid
        )
