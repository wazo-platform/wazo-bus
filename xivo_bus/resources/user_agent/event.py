# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import UserEvent
from ..common.types import Format


class UserAgentAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_agent_associated'
    routing_key_fmt = 'config.users.{user_uuid}.agents.updated'

    def __init__(
        self,
        agent_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
        user_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'user_uuid': str(user_uuid),
            'agent_id': agent_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserAgentDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_agent_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.agents.deleted'

    def __init__(
        self,
        agent_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
        user_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'user_uuid': str(user_uuid),
            'agent_id': agent_id,
        }
        super().__init__(content, tenant_uuid, user_uuid)
