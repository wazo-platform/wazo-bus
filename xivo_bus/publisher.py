# Copyright 2012-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from .base import Base
from .mixins import PublisherMixin, QueuePublisherMixin, ThreadableMixin, WazoEventMixin

logger = logging.getLogger(__name__)


class BusPublisher(WazoEventMixin, PublisherMixin, Base):
    def __init__(
        self,
        name=None,
        service_uuid=None,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name='',
        exchange_type='',
        **kwargs
    ):
        super().__init__(
            name=name,
            service_uuid=service_uuid,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            **kwargs
        )


# Deprecated, thread should be avoided to respect WPEP-0004
class BusPublisherWithQueue(WazoEventMixin, ThreadableMixin, QueuePublisherMixin, Base):
    def __init__(
        self,
        name=None,
        service_uuid=None,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name='',
        exchange_type='',
        **kwargs
    ):
        super().__init__(
            name=name,
            service_uuid=service_uuid,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            **kwargs
        )
