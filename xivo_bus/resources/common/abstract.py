# -*- coding: utf-8 -*-
# Copyright 2022-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import re

from inspect import isabstract
from abc import ABCMeta, abstractmethod
from six import with_metaclass


def camel_to_snake(name):
    name = name.split('Event')[0]
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class EventMeta(ABCMeta):
    def __new__(mcs, name, bases, attrs):
        cls = super(EventMeta, mcs).__new__(mcs, name, bases, attrs)
        if not isabstract(cls) and 'name' not in attrs:
            setattr(cls, 'name', camel_to_snake(name))
        return cls


class AbstractEvent(with_metaclass(EventMeta, object)):
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
    def routing_key_fmt(self):
        pass

    @property
    def routing_key(self):
        variables = dict(**self.content)
        variables.update(name=self.name, **vars(self))
        return self.routing_key_fmt.format(**variables)

    @property
    def required_acl(self):
        """
        Deprecated, use required_access instead
        """
        if hasattr(self, 'required_acl_fmt'):
            variables = dict(**self.content)
            variables.update(name=self.name, **vars(self))
            return self.required_acl_fmt.format(**variables)
        return 'events.{}'.format(self.routing_key)

    @property
    def required_access(self):
        return 'event.{}'.format(self.name)

    @property
    def headers(self):
        variables = vars(self)
        return dict(name=self.name, **variables)

    def marshal(self):
        return self.content
