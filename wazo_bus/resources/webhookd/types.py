from typing import Any, TypedDict

from wazo_bus.resources.common.types import UUIDStr


class _BaseSubscription(TypedDict, total=False):
    uuid: UUIDStr
    name: str
    url: str
    events: list[str]
    service: str
    config: dict[str, Any]
    metadata: dict[str, Any]


class UserSubscription(_BaseSubscription):
    pass


class Subscription(_BaseSubscription, total=False):
    events_user_uuid: str
    events_wazo_uuid: str
    owner_user_uuid: str
    owner_tenant_uuid: str
