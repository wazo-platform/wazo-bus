# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABCMeta, abstractmethod
from six import with_metaclass


class AbstractEvent(with_metaclass(ABCMeta, object)):
    __slots__ = ('content',)

    def __init__(self, content=None):
        self.content = content or {}

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.content == other.content
            and vars(self) == vars(other)
        )

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<Event: {} (headers: {}, content: {})>'.format(
            self.name,
            self.headers,
            self.content,
        )

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def routing_key_fmt(self):
        pass

    @property
    def routing_key(self):
        variables = dict(**self.content)
        variables.update(vars(self), name=self.name)
        return self.routing_key_fmt.format(**variables)

    @property
    def required_acl(self):
        """
        Deprecated, use required_access instead
        """
        if hasattr(self, 'required_acl_fmt'):
            variables = dict(**self.content)
            variables.update(vars(self), name=self.name)
            return self.required_acl_fmt.format(**variables)
        return 'events.{}'.format(self.routing_key)

    @property
    def required_access(self):
        return 'event.{}'.format(self.name)

    @property
    def headers(self):
        headers = dict(vars(self))
        headers.update(name=self.name)
        return headers

    def marshal(self):
        return self.content
