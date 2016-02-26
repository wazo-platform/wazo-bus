# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
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


class CollectdEvent(object):
    interval = 10
    plugin = None
    plugin_instance = None
    type_ = None
    type_instance = None
    values = ()
    time = 'N'

    def is_valid(self):
        return (self.plugin is not None and
                self.plugin_instance is not None and
                self.type_ is not None and
                self.type_instance is not None and
                (self.time == 'N' or isinstance(self.time, int)) and
                len(self.values) > 0)
