# -*- coding: utf-8 -*-
# Copyright 2012-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json


class InvalidMessage(ValueError):
    pass


class Marshaler(object):

    content_type = 'application/json'

    def __init__(self, uuid):
        self._uuid = uuid

    def metadata(self, command):
        result = {
            'name': command.name,
            'origin_uuid': self._uuid,
        }

        if hasattr(command, 'required_acl'):
            result['required_acl'] = command.required_acl

        return result

    def marshal_message(self, command):
        body = dict(self.metadata(command))
        body['data'] = command.marshal()
        return json.dumps(body)

    @classmethod
    def unmarshal_message(cls, obj, event_class):
        if not isinstance(obj, dict):
            raise InvalidMessage(obj)
        if 'data' not in obj:
            raise InvalidMessage(obj)
        if 'origin_uuid' not in obj:
            raise InvalidMessage(obj)

        event = event_class.unmarshal(obj['data'])
        event.metadata = {'origin_uuid': obj['origin_uuid']}
        return event


class CollectdMarshaler(object):

    content_type = 'text/collectd'

    def __init__(self, uuid):
        self._uuid = uuid

    def marshal_message(self, command):
        if not command.is_valid():
            raise ValueError(command)

        message = 'PUTVAL {host}/{plugin}/{type_}-{type_instance} interval={interval} {time}:{values}'

        if command.plugin_instance:
            plugin = '{}-{}'.format(command.plugin, command.plugin_instance)
        else:
            plugin = command.plugin

        return message.format(
            host=self._uuid,
            plugin=plugin,
            type_=command.type_,
            type_instance=command.type_instance,
            interval=command.interval,
            time=command.time,
            values=':'.join(command.values)
        )

    def metadata(self, _):
        return {}
