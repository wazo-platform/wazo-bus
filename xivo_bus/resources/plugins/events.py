# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class _ProgressEvent(object):

    def __init__(self, uuid_, status, errors=None):
        self._uuid = uuid_
        self._status = status
        self._errors = errors
        self.routing_key = self.routing_key_fmt.format(uuid=uuid_, status=status)
        self.required_acl = 'events.{}'.format(self.routing_key)

    def marshal(self):
        data = {
            'uuid': self._uuid,
            'status': self._status,
        }

        if self._errors:
            data['errors'] = self._errors

        return data

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        errors = ', errors={!r}'.format(self._errors) if self._errors is not None else ''
        return '{}({!r}, {!r}{})'.format(
            self.__class__.__name__,
            self._uuid,
            self._status,
            errors,
        )

    @classmethod
    def unmarshal(cls, body):
        uuid_ = body.pop('uuid')
        status = body.pop('status')
        return cls(uuid_, status, **body)


class PluginInstallProgressEvent(_ProgressEvent):

    name = 'plugin_install_progress'
    routing_key_fmt = 'plugin.install.{uuid}.{status}'


class PluginUninstallProgressEvent(_ProgressEvent):

    name = 'plugin_uninstall_progress'
    routing_key_fmt = 'plugin.uninstall.{uuid}.{status}'
