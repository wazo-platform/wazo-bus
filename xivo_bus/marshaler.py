# -*- coding: utf-8 -*-

# Copyright (C) 2012-2016 Avencall
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

import json


class Marshaler(object):

    content_type = 'application/json'

    def __init__(self, uuid):
        self._uuid = uuid

    def marshal_message(self, command):
        return json.dumps({'name': command.name,
                           'origin_uuid': self._uuid,
                           'data': command.marshal()})

    def unmarshal_message(self, data):
        return json.loads(data)
