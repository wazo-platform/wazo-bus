# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseIngressHTTPEvent(BaseEvent):
    def __init__(self, ingress_http):
        self._body = ingress_http
        super(_BaseIngressHTTPEvent, self).__init__()


class CreateIngressHTTPEvent(_BaseIngressHTTPEvent):
    name = 'ingress_http_created'
    routing_key_fmt = 'config.ingresses.http.created'


class EditIngressHTTPEvent(_BaseIngressHTTPEvent):
    name = 'ingress_http_updated'
    routing_key_fmt = 'config.ingresses.http.updated'


class DeleteIngressHTTPEvent(_BaseIngressHTTPEvent):
    name = 'ingress_http_deleted'
    routing_key_fmt = 'config.ingresses.http.deleted'
