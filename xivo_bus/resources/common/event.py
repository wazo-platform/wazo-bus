# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections.abc import Mapping

from .abstract import EventProtocol
from .types import UUIDStr


class ServiceEvent(EventProtocol):
    '''
    ### Service-level event base class

    These events are intended for internal use by services and will never
    make it through the websocket.
    '''

    def __init__(self, content: Mapping | None = None):
        self.content = content or {}


class TenantEvent(ServiceEvent):
    '''
    ### Tenant-level event base class

    These events are intended for *all* users of the specified tenant.  They will be
    dispatched to all it's connected users by setting `user_uuid:*` in the headers.

    #### Required property:
        - tenant_uuid
    '''

    def __init__(self, content: Mapping | None, tenant_uuid: UUIDStr):
        super().__init__(content)
        if tenant_uuid is None:
            raise ValueError('tenant_uuid must have a value')
        self.tenant_uuid = str(tenant_uuid)
        setattr(self, 'user_uuid:*', True)


class UserEvent(TenantEvent):
    '''
    ### User-level event base class

    These events are intended for a single user from a specific tenant.  They will be
    dispatched through the websocket to the user by setting `user_uuid:{uuid}`
    in the headers.

    #### Required properties:
        - tenant_uuid
        - user_uuid
    '''

    def __init__(
        self,
        content: Mapping | None,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr | None,
    ):
        super().__init__(content, tenant_uuid)
        delattr(self, 'user_uuid:*')
        self.user_uuid = str(user_uuid) if user_uuid else None

    @property
    def headers(self) -> dict:
        headers = super().headers
        uuid = headers.pop('user_uuid')
        if uuid:
            headers[f'user_uuid:{uuid}'] = True
        return headers


class MultiUserEvent(TenantEvent):
    '''
    ### User-level event base class (targetting multiple users)

    These events are intended for multiple users from a specific tenant.
    They will be dispatched through the websocket by setting `user_uuid:{uuid} = True`
    in the headers for all intended users.

    #### Required properties:
        - tenant_uuid
        - list of user_uuids
    '''

    __slots__ = ('user_uuids',)

    def __init__(
        self,
        content: Mapping | None,
        tenant_uuid: UUIDStr,
        user_uuids: list[UUIDStr],
    ):
        super().__init__(content, tenant_uuid)
        delattr(self, 'user_uuid:*')
        if not isinstance(user_uuids, list):
            raise ValueError('user_uuids must be a list of uuids')
        self.user_uuids = [str(user_uuid) for user_uuid in user_uuids]

    @property
    def headers(self) -> dict:
        headers = super().headers
        for user_uuid in self.user_uuids:
            headers[f'user_uuid:{user_uuid}'] = True
        return headers
