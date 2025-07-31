# Copyright 2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ..common.event import TenantEvent, UserEvent
from ..common.types import UUIDStr
from .types import Subscription, UserSubscription


class WebhookdSubscriptionCreatedEvent(TenantEvent):
    service = 'webhookd'
    name = 'webhookd_subscription_created'
    routing_key_fmt = 'webhookd.subscription.created'

    def __init__(
        self,
        subscription: Subscription,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(subscription, tenant_uuid)


class WebhookdSubscriptionCreatedUserEvent(UserEvent):
    service = 'webhookd'
    name = 'webhookd_user_subscription_created'
    routing_key_fmt = 'webhookd.users.{user_uuid}.subscription.created'

    def __init__(
        self,
        subscription: UserSubscription,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(subscription, tenant_uuid, user_uuid)


class WebhookdSubscriptionUpdatedEvent(TenantEvent):
    service = 'webhookd'
    name = 'webhookd_subscription_updated'
    routing_key_fmt = 'webhookd.subscription.updated'

    def __init__(
        self,
        subscription: Subscription,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(subscription, tenant_uuid)


class WebhookdSubscriptionUpdatedUserEvent(UserEvent):
    service = 'webhookd'
    name = 'webhookd_user_subscription_updated'
    routing_key_fmt = 'webhookd.users.{user_uuid}.subscription.updated'

    def __init__(
        self,
        subscription: UserSubscription,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(subscription, tenant_uuid, user_uuid)


class WebhookdSubscriptionDeletedEvent(TenantEvent):
    service = 'webhookd'
    name = 'webhookd_subscription_deleted'
    routing_key_fmt = 'webhookd.subscription.deleted'

    def __init__(
        self,
        subscription: Subscription,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(subscription, tenant_uuid)


class WebhookdSubscriptionDeletedUserEvent(UserEvent):
    service = 'webhookd'
    name = 'webhookd_user_subscription_deleted'
    routing_key_fmt = 'webhookd.users.{user_uuid}.subscription.deleted'

    def __init__(
        self,
        subscription: UserSubscription,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        super().__init__(subscription, tenant_uuid, user_uuid)
