# Copyright 2013-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


from unittest import TestCase
from hamcrest import assert_that, equal_to
from uuid import uuid4

from ..event import ServiceEvent, TenantEvent, UserEvent, MultiUserEvent

TENANT_UUID = uuid4()
USER_UUID = uuid4()
USER2_UUID = uuid4()
USER3_UUID = uuid4()


class SomeServiceEvent(ServiceEvent):
    name = 'some_service_event'
    routing_key_fmt = 'some.service.event'

    def __init__(self, a, b):
        content = {'a': a, 'b': b}
        super().__init__(content)


class SomeTenantEvent(TenantEvent):
    name = 'some_tenant_event'
    routing_key_fmt = 'some.tenant.event'

    def __init__(self, a, b, tenant_uuid):
        content = {'a': a, 'b': b}
        super().__init__(content, tenant_uuid)


class SomeUserEvent(UserEvent):
    name = 'some_user_event'
    routing_key_fmt = 'some.user.event'

    def __init__(self, a, b, tenant_uuid, user_uuid):
        content = {'a': a, 'b': b}
        super().__init__(content, tenant_uuid, user_uuid)


class SomeMultiUserEvent(MultiUserEvent):
    name = 'some_multi_user_event'
    routing_key_fmt = 'some.multi.user.event'

    def __init__(self, a, b, tenant_uuid, user_uuids):
        content = {'a': a, 'b': b}
        super().__init__(content, tenant_uuid, user_uuids)


class TestServiceEvent(TestCase):
    def setUp(self):
        self.event = SomeServiceEvent(1, 2)

    def test_headers(self):
        assert_that(self.event.headers, equal_to({'name': 'some_service_event'}))

    def test_marshal(self):
        assert_that(
            self.event.marshal(),
            equal_to(
                {
                    'a': 1,
                    'b': 2,
                }
            ),
        )


class TestTenantEvent(TestCase):
    def setUp(self):
        self.event = SomeTenantEvent(1, 2, TENANT_UUID)

    def test_headers(self):
        assert_that(
            self.event.headers,
            equal_to(
                {
                    'name': 'some_tenant_event',
                    'user_uuid:*': True,
                    'tenant_uuid': str(TENANT_UUID),
                }
            ),
        )

    def test_marshal(self):
        assert_that(
            self.event.marshal(),
            equal_to(
                {
                    'a': 1,
                    'b': 2,
                }
            ),
        )


class TestUserEvent(TestCase):
    def setUp(self):
        self.event = SomeUserEvent(1, 2, TENANT_UUID, USER_UUID)

    def test_headers(self):
        assert_that(
            self.event.headers,
            equal_to(
                {
                    'name': 'some_user_event',
                    'tenant_uuid': str(TENANT_UUID),
                    f'user_uuid:{USER_UUID}': True,
                }
            ),
        )

    def test_marshal(self):
        assert_that(
            self.event.marshal(),
            equal_to(
                {
                    'a': 1,
                    'b': 2,
                }
            ),
        )


class TestMultiUserEvent(TestCase):
    def setUp(self):
        self.event = SomeMultiUserEvent(
            5, 6, TENANT_UUID, [USER_UUID, USER2_UUID, USER3_UUID]
        )

    def test_headers(self):
        assert_that(
            self.event.headers,
            equal_to(
                {
                    'name': 'some_multi_user_event',
                    'tenant_uuid': str(TENANT_UUID),
                    f'user_uuid:{USER_UUID}': True,
                    f'user_uuid:{USER2_UUID}': True,
                    f'user_uuid:{USER3_UUID}': True,
                }
            ),
        )

    def test_marshal(self):
        assert_that(
            self.event.marshal(),
            equal_to(
                {
                    'a': 5,
                    'b': 6,
                }
            ),
        )
