# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
import logging

from flask import Flask


# Configure logger
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

debug, info, warn, error = (
    logger.debug,
    logger.info,
    logger.warning,
    logger.error
)


# Configure Flask
app = Flask('bus-services')

from bus_test import routes  # noqa
routes._bus.start()
