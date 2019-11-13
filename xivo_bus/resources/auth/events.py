# -*- coding: utf-8 -*-
# Copyright 2017-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import BaseEvent


class _BaseExternalAuthEvent(BaseEvent):

    def __init__(self, user_uuid, external_auth_name):
        self._body = dict(user_uuid=str(user_uuid), external_auth_name=external_auth_name)
        super(_BaseExternalAuthEvent, self).__init__()


class TenantCreatedEvent(BaseEvent):

    name = 'auth_tenant_added'
    routing_key_fmt = 'auth.tenants.{uuid}.created'

    def __init__(self, uuid, name):
        self._body = {'uuid': uuid, 'name': name}
        super(TenantCreatedEvent, self).__init__()


class TenantUpdatedEvent(BaseEvent):

    name = 'auth_tenant_updated'
    routing_key_fmt = 'auth.tenants.{uuid}.updated'

    def __init__(self, uuid, name):
        self._body = {'uuid': uuid, 'name': name}
        super(TenantUpdatedEvent, self).__init__()


class TenantDeletedEvent(BaseEvent):

    name = 'auth_tenant_deleted'
    routing_key_fmt = 'auth.tenants.{uuid}.deleted'

    def __init__(self, uuid):
        self._body = {'uuid': uuid}
        super(TenantDeletedEvent, self).__init__()


class UserExternalAuthAdded(_BaseExternalAuthEvent):

    name = 'auth_user_external_auth_added'
    routing_key_fmt = 'auth.users.{user_uuid}.external.{external_auth_name}.created'


class UserExternalAuthAuthorized(_BaseExternalAuthEvent):

    name = 'auth_user_external_auth_authorized'
    routing_key_fmt = 'auth.users.{user_uuid}.external.{external_auth_name}.authorized'


class UserExternalAuthDeleted(_BaseExternalAuthEvent):

    name = 'auth_user_external_auth_deleted'
    routing_key_fmt = 'auth.users.{user_uuid}.external.{external_auth_name}.deleted'


class RefreshTokenCreatedEvent(BaseEvent):

    name = 'auth_refresh_token_created'
    routing_key_fmt = 'auth.users.{user_uuid}.tokens.{client_id}.created'

    def __init__(self, user_uuid, client_id, mobile, tenant_uuid, **ignored):
        self._body = {
            'user_uuid': user_uuid,
            'client_id': client_id,
            'tenant_uuid': tenant_uuid,
            'mobile': mobile,
        }
        super(RefreshTokenCreatedEvent, self).__init__()


class RefreshTokenDeletedEvent(BaseEvent):

    name = 'auth_refresh_token_deleted'
    routing_key_fmt = 'auth.users.{user_uuid}.tokens.{client_id}.deleted'

    def __init__(self, user_uuid, client_id, mobile, tenant_uuid, **ignored):
        self._body = {
            'user_uuid': user_uuid,
            'client_id': client_id,
            'tenant_uuid': tenant_uuid,
            'mobile': mobile,
        }
        super(RefreshTokenDeletedEvent, self).__init__()


class SessionCreatedEvent(BaseEvent):

    name = 'auth_session_created'
    routing_key_fmt = 'auth.sessions.{uuid}.created'

    def __init__(self, uuid, tenant_uuid, user_uuid, **kwargs):
        self._body = {
            'uuid': uuid,
            'tenant_uuid': tenant_uuid,
            'user_uuid': user_uuid,
            'mobile': kwargs.get('mobile', False),
        }
        super(SessionCreatedEvent, self).__init__()


class SessionDeletedEvent(BaseEvent):

    name = 'auth_session_deleted'
    routing_key_fmt = 'auth.sessions.{uuid}.deleted'

    def __init__(self, uuid, tenant_uuid, user_uuid):
        self._body = {
            'uuid': uuid,
            'tenant_uuid': tenant_uuid,
            'user_uuid': user_uuid,
        }
        super(SessionDeletedEvent, self).__init__()


class SessionExpireSoonEvent(BaseEvent):

    name = 'auth_session_expire_soon'
    routing_key_fmt = 'auth.users.{user_uuid}.sessions.{uuid}.expire_soon'

    def __init__(self, uuid, tenant_uuid, user_uuid):
        self._body = {
            'uuid': uuid,
            'tenant_uuid': tenant_uuid,
            'user_uuid': user_uuid,
        }
        super(SessionExpireSoonEvent, self).__init__()
