# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import sys
from collections import defaultdict, namedtuple
from threading import Lock

from flask import Flask, jsonify, request

from wazo_bus.base import Base
from wazo_bus.mixins import ConsumerMixin, QueuePublisherMixin, ThreadableMixin

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger("remote-bus-pilot")


class Bus(ThreadableMixin, QueuePublisherMixin, ConsumerMixin, Base):
    pass


class MessageBroker:
    Handler = namedtuple('Handler', 'handler, headers, routing_key')

    def __init__(self):
        self._messages = defaultdict(list)
        self._handlers = defaultdict(list)
        self.lock = Lock()

    def _filter_headers(self, headers):
        headers = headers or {}
        return {k: v for k, v in headers.items() if not k.startswith('x-')}

    def enqueue(self, event, message):
        with self.lock:
            self._messages[event].append(message)

    def dequeue(self, event):
        with self.lock:
            return self._messages.pop(event, [])

    def count(self, event):
        with self.lock:
            return len(self._messages[event])

    def bind_handler(self, event, handler, headers=None, routing_key=None):
        handler = self.Handler(handler, self._filter_headers(headers), routing_key)
        with self.lock:
            self._handlers[event].append(handler)

    def get_handlers(self, event):
        with self.lock:
            return self._handlers[event].copy()

    def unbind_handler(self, event, headers=None, routing_key=None):
        headers = self._filter_headers(headers)
        with self.lock:
            for idx, handler in enumerate(self._handlers[event]):
                if handler.headers == headers and handler.routing_key == routing_key:
                    self._handlers[event].pop(idx)
                    return handler.handler


info, error = logger.info, logger.error
app = Flask('remote-bus-pilot')
bus = Bus(
    name='remote-bus',
    host='rabbitmq',
    exchange_name=os.getenv('EXCHANGE_NAME'),
    exchange_type=os.getenv('EXCHANGE_TYPE'),
)
broker = MessageBroker()


def create_event_handler(event, headers=None, routing_key=None):
    def _store_message(payload):
        broker.enqueue(event, payload)

    info('created event handler for event \'%s\' with headers (%s)', event, headers)
    broker.bind_handler(event, _store_message, headers, routing_key)
    return _store_message


def process_json(event, jsondata, use_match=False):
    headers = dict(jsondata.get('headers', None) or {}, name=event)
    payload = jsondata.get('payload', None) or {}
    headers_match_all = jsondata.get('headers_match_all', True)
    routing_key = jsondata.get('routing_key', None)

    if use_match:
        headers.setdefault('x-match', 'all' if headers_match_all else 'any')

    return headers, routing_key, payload


def make_response(code, status=None, **kwargs):
    return jsonify({'result': code, 'status': status, **kwargs}), code


#####################
# Routes definition #
#####################
@app.route('/bus/status', methods=['GET'])
def status():
    return make_response(200, None, running=bus.consumer_connected())


@app.route('/bus/<string:event>/publish', methods=['POST'])
def publish(event):
    headers, routing_key, payload = process_json(event, request.json)

    try:
        bus.publish(event, headers=headers, routing_key=routing_key, payload=payload)
        info(
            'Published to \'%s\' (headers: %s, routing_key: %s)',
            event,
            headers,
            routing_key,
        )
    except Exception:
        error('Publishing failed', exc_info=1)
        return make_response(400, 'An error occured, message was not sent on bus')

    return make_response(
        200,
        'Message succesfully sent on bus',
        message=payload,
        headers=headers,
        routing_key=routing_key,
    )


@app.route('/bus/<string:event>/subscribe', methods=['POST'])
def subscribe(event):
    headers, routing_key, _ = process_json(event, request.json, use_match=True)
    handler = create_event_handler(event, headers, routing_key)
    bus.subscribe(event, handler, headers, routing_key)
    info('Subscribed to \'%s\' (headers: %s)', event, headers)
    return make_response(
        200,
        'Registered event handler',
        event=event,
        headers=headers,
        routing_key=routing_key,
    )


@app.route('/bus/<string:event>/unsubscribe', methods=['POST'])
def unsubscribe(event):
    headers, routing_key, _ = process_json(event, request.json)

    handler = broker.unbind_handler(event, headers, routing_key)
    if handler:
        bus.unsubscribe(event, handler)
        info('Unsubscribed from \'%s\' (headers: %s)', event, headers)
        return make_response(200, 'Unregistered event handler', event=event)
    return make_response(400, 'Handler not found', event=event)


@app.route('/bus/<string:event>/messages', methods=['GET'])
def get_messages(event):
    return jsonify(broker.dequeue(event))


@app.route('/bus/<string:event>/messages/count', methods=['GET'])
def get_messages_count(event):
    return jsonify(broker.count(event))


if __name__ == '__main__':
    with bus:
        app.run(host='0.0.0.0', port=5000)
