# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .base import Base
from .mixins import ConsumerMixin, ThreadableMixin, WazoEventMixin


class BusConsumer(WazoEventMixin, ThreadableMixin, ConsumerMixin, Base):
    def __init__(
        self,
        name=None,
        username='guest',
        password='guest',
        host='localhost',
        port=5672,
        exchange_name='',
        exchange_type='',
        subscribe=None,
        **kwargs
    ):
        super().__init__(
            name=name,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            subscribe=subscribe,
            **kwargs
        )
