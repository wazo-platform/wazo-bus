# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class BaseApplicationEvent(object):

    def __init__(self, app_uuid):
        self.uuid = str(app_uuid)

    def marshal(self):
        return {'uuid': self.uuid}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['uuid'])

    def __eq__(self, other):
        return self.uuid == other.uuid

    def __ne__(self, other):
        return self.uuid != other.uuid


class EditApplicationEvent(BaseApplicationEvent):
    name = 'application_edited'
    routing_key = 'config.applications.edited'


class CreateApplicationEvent(BaseApplicationEvent):
    name = 'application_created'
    routing_key = 'config.applications.created'


class DeleteApplicationEvent(BaseApplicationEvent):
    name = 'application_deleted'
    routing_key = 'config.applications.deleted'
