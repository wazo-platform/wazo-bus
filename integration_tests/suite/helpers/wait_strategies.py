# Copyright 2022-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_test_helpers import until
from kombu import Connection


def wait_for_rabbitmq(integration_test):
    def try_connect(connection):
        try:
            connection.connect()
        except Exception:
            return False
        else:
            connection.release()
            return True

    port = integration_test.service_port(5672, 'rabbitmq')
    with Connection(f'amqp://guest:guest@127.0.0.1:{port}//') as connection:
        until.true(try_connect, connection, timeout=30)
