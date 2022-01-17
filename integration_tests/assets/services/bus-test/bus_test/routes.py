# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
from flask import request, jsonify
from xivo_bus.base import BusConnector

from . import app, info, error
from .bus import MessageBroker, MiddlewareManager


_bus = BusConnector(
    host='rabbitmq',
    exchange_name=os.getenv('EXCHANGE_NAME'),
    exchange_type=os.getenv('EXCHANGE_TYPE'),
)
_broker = MessageBroker()
_middlewares = MiddlewareManager()


def create_event_handler(event, headers=None, routing_key=None):
    def _store_message(payload):
        _broker.enqueue(event, payload)

    info('created event handler for event \'%s\' with headers (%s)', event, headers)
    _broker.bind_handler(event, _store_message, headers, routing_key)
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
@app.route('/bus/<string:event>/publish', methods=['POST'])
def publish(event):
    headers, routing_key, payload = process_json(event, request.json)

    try:
        _bus.publish(event, headers=headers, routing_key=routing_key, payload=payload)
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
    _bus.subscribe(event, handler, headers, routing_key)
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

    handler = _broker.unbind_handler(event, headers, routing_key)
    if handler:
        _bus.unsubscribe(event, handler)
        info('Unsubscribed from \'%s\' (headers: %s)', event, headers)
        return make_response(200, 'Unregistered event handler', event=event)
    return make_response(400, 'Handler not found', event=event)


@app.route('/bus/<string:event>/messages', methods=['GET'])
def get_messages(event):
    return jsonify(_broker.dequeue(event))


@app.route('/bus/middlewares', methods=['GET'])
def middleware():
    return make_response(200, middlewares=_middlewares.all)


@app.route('/bus/middlewares/<string:name>', methods=['PUT', 'DELETE'])
def modify_middleware(name):
    middleware = _middlewares.get(name)
    if not middleware:
        return make_response(404, 'Middleware \'{}\' could not be found'.format(name))

    json_ = request.json or {}
    args = json_.get('args', {})
    kwargs = json_.get('kwargs', {})

    if request.method == 'PUT':
        try:
            _bus.register_middleware(middleware(*args, **kwargs))
        except Exception as exc:
            return make_response(400, error=str(exc))
        return make_response(200, 'Registered middleware succesfully', middleware=name)
    elif request.method == 'DELETE':
        if not _bus.unregister_middleware(middleware):
            return make_response(
                404, 'Requested middleware not found on bus', middleware=name
            )
        return make_response(
            200, 'Unregistered middleware succesfully', middleware=name
        )
