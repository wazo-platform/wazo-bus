# -*- coding: utf-8 -*-

# Copyright (C) 2016 Proformatique Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditGroupEvent(ResourceConfigEvent):
    name = 'group_edited'
    routing_key = 'config.groups.edited'


class CreateGroupEvent(ResourceConfigEvent):
    name = 'group_created'
    routing_key = 'config.groups.created'


class DeleteGroupEvent(ResourceConfigEvent):
    name = 'group_deleted'
    routing_key = 'config.groups.deleted'


class EditGroupFallbackEvent(ResourceConfigEvent):
    name = 'group_fallback_edited'
    routing_key = 'config.groups.fallbacks.edited'
