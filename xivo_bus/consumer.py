# Copyright 2020-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from .base import Base
from .mixins import ThreadableMixin, ConsumerMixin, InitMixin


class BusConsumer(InitMixin, ThreadableMixin, ConsumerMixin, Base):
    pass
