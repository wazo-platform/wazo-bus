# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class FaxOutboundCreated(BaseEvent):

    name = 'fax_outbound_created'
    routing_key_fmt = 'faxes.outbound.created'

    def __init__(self, fax_infos):
        self._body = fax_infos
        super(FaxOutboundCreated, self).__init__()


class FaxOutboundSucceeded(BaseEvent):

    name = 'fax_outbound_succeeded'
    routing_key_fmt = 'faxes.outbound.{id}.succeeded'

    def __init__(self, fax_infos):
        self._body = fax_infos
        super(FaxOutboundSucceeded, self).__init__()


class FaxOutboundFailed(BaseEvent):

    name = 'fax_outbound_failed'
    routing_key_fmt = 'faxes.outbound.{id}.failed'

    def __init__(self, fax_infos):
        self._body = fax_infos
        super(FaxOutboundFailed, self).__init__()


class FaxOutboundUserCreated(BaseEvent):

    name = 'fax_outbound_user_created'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.created'

    def __init__(self, fax_infos):
        self._body = fax_infos
        super(FaxOutboundUserCreated, self).__init__()


class FaxOutboundUserSucceeded(BaseEvent):

    name = 'fax_outbound_user_succeeded'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.succeeded'

    def __init__(self, fax_infos):
        self._body = fax_infos
        super(FaxOutboundUserSucceeded, self).__init__()


class FaxOutboundUserFailed(BaseEvent):

    name = 'fax_outbound_user_failed'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.failed'

    def __init__(self, fax_infos):
        self._body = fax_infos
        super(FaxOutboundUserFailed, self).__init__()
