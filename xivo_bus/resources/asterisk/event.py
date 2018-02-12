# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


class _AsteriskReloadProgress(object):

    def __init__(self, uuid, status, command):
        self._body = {'uuid': uuid, 'status': status, 'command': command}
        self.routing_key = self.routing_key_fmt.format(uuid=uuid, status=status)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        return self._body

    def __ne__(self, other):
        return not self._body == other._body

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self._body == other._body

    @classmethod
    def unmarshal(cls, body):
        return cls(**body)


class AsteriskReloadProgressEvent(_AsteriskReloadProgress):

    name = 'asterisk_reload_progress'
    routing_key_fmt = 'sysconfd.asterisk.reload.{uuid}.{status}'
