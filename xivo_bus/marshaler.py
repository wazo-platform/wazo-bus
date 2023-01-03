# Copyright 2012-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class InvalidMessage(ValueError):
    pass


class CollectdMarshaler:

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
            values=':'.join(command.values),
        )

    def metadata(self, _):
        return {}
