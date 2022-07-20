# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class IAXGeneralEditedEvent(ServiceEvent):
    name = 'iax_general_edited'
    routing_key_fmt = 'config.iax_general.edited'

    def __init__(self):
        super(IAXGeneralEditedEvent, self).__init__()
