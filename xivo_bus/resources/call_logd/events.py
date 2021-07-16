# -*- coding: utf-8 -*-
# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import BaseEvent


class RetentionUpdatedEvent(BaseEvent):

    name = 'call_logd_retention_updated'
    routing_key_fmt = 'call_logd.retention.updated'

    def __init__(self, retention):
        self._body = retention
        super(RetentionUpdatedEvent, self).__init__()


class ExportCreatedEvent(BaseEvent):

    name = 'call_logd_export_created'
    routing_key_fmt = 'call_logd.export.created'

    def __init__(self, export):
        self._body = export
        super(ExportCreatedEvent, self).__init__()


class ExportUpdatedEvent(BaseEvent):

    name = 'call_logd_export_updated'
    routing_key_fmt = 'call_logd.export.updated'

    def __init__(self, export):
        self._body = export
        super(ExportUpdatedEvent, self).__init__()
