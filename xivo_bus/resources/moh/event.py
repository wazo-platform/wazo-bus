# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseMohEvent(BaseEvent):

    def __init__(self, moh):
        self._body = moh
        super(_BaseMohEvent, self).__init__()


class EditMohEvent(_BaseMohEvent):
    name = 'moh_edited'
    routing_key_fmt = 'config.moh.edited'


class CreateMohEvent(_BaseMohEvent):
    name = 'moh_created'
    routing_key_fmt = 'config.moh.created'


class DeleteMohEvent(_BaseMohEvent):
    name = 'moh_deleted'
    routing_key_fmt = 'config.moh.deleted'
