# -*- coding: utf-8 -*-
# Copyright (C) 2014-2016 Avencall
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class FuncKeyTemplateEvent(ResourceConfigEvent):
    routing_key = 'config.funckey.template.{}'


class CreateFuncKeyTemplateEvent(ResourceConfigEvent):
    name = 'func_key_template_created'
    routing_key = FuncKeyTemplateEvent.routing_key.format('created')


class DeleteFuncKeyTemplateEvent(ResourceConfigEvent):
    name = 'func_key_template_deleted'
    routing_key = FuncKeyTemplateEvent.routing_key.format('deleted')


class EditFuncKeyTemplateEvent(ResourceConfigEvent):
    name = 'func_key_template_edited'
    routing_key = FuncKeyTemplateEvent.routing_key.format('edited')


class UserFuncKeyEvent(ResourceConfigEvent):
    routing_key = 'config.user.{}'

    def __init__(self, func_key_id, user_id):
        self.func_key_id = func_key_id
        self.user_id = user_id

    def marshal(self):
        return {'id': self.func_key_id,
                'destination': 'user',
                'user_id': self.user_id}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['user_id'])


class BSFilterFuncKeyEvent(ResourceConfigEvent):
    routing_key = 'config.bsfilter.{}'

    def __init__(self, func_key_id, filter_id, secretary_id):
        self.func_key_id = func_key_id
        self.filter_id = filter_id
        self.secretary_id = secretary_id

    def marshal(self):
        return {'id': self.func_key_id,
                'destination': 'bsfilter',
                'filter_id': self.filter_id,
                'secretary_id': self.secretary_id}

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['filter_id'], msg['secretary_id'])


class UserCreateFuncKeyEvent(UserFuncKeyEvent):
    name = 'func_key_created'
    routing_key = UserFuncKeyEvent.routing_key.format('created')


class UserDeleteFuncKeyEvent(UserFuncKeyEvent):
    name = 'func_key_deleted'
    routing_key = UserFuncKeyEvent.routing_key.format('deleted')


class BSFilterCreateFuncKeyEvent(BSFilterFuncKeyEvent):
    name = 'func_key_created'
    routing_key = BSFilterFuncKeyEvent.routing_key.format('created')


class BSFilterDeleteFuncKeyEvent(BSFilterFuncKeyEvent):
    name = 'func_key_deleted'
    routing_key = BSFilterFuncKeyEvent.routing_key.format('deleted')
