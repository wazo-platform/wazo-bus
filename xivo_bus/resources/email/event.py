# -*- coding: utf-8 -*-
# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class EmailConfigUpdatedEvent(ServiceEvent):
    name = 'email_config_updated'
    routing_key_fmt = 'config.email.updated'

    def __init__(self):
        super(EmailConfigUpdatedEvent, self).__init__()
