# -*- coding: utf-8 -*-
# Copyright 2017-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest import TestCase
from uuid import uuid4
from hamcrest import assert_that, equal_to
from ..events import PluginInstallProgressEvent, PluginUninstallProgressEvent


def new_uuid():
    return str(uuid4())


class TestPluginInstallProgressEvent(TestCase):

    def test_marshal(self):
        uuid_ = new_uuid()
        status = 'start'

        event = PluginInstallProgressEvent(uuid_, status)

        result = event.marshal()
        expected = {'uuid': uuid_, 'status': status}

        assert_that(result, equal_to(expected))

    def test_marshal_on_error(self):
        uuid_ = new_uuid()
        status = 'error'
        errors = {
            'error_id': 'packaging-error',
            'message': 'Packaging Error',
            'resource': 'plugins',
            'details': {},
        }

        event = PluginInstallProgressEvent(uuid_, status, errors=errors)

        result = event.marshal()
        expected = {'uuid': uuid_, 'status': status, 'errors': errors}

        assert_that(result, equal_to(expected))

    def test_unmarshal(self):
        uuid_ = new_uuid()
        status = 'building'

        body = {'uuid': uuid_, 'status': status}
        event = PluginInstallProgressEvent.unmarshal(body)
        expected = PluginInstallProgressEvent(uuid_, status)

        assert_that(event, equal_to(expected))

    def test_unmarshal_on_error(self):
        uuid_ = new_uuid()
        status = 'building'
        errors = {
            'error_id': 'packaging-error',
            'message': 'Packaging Error',
            'resource': 'plugins',
            'details': {},
        }

        body = {'uuid': uuid_, 'status': status, 'errors': errors}
        event = PluginInstallProgressEvent.unmarshal(body)
        expected = PluginInstallProgressEvent(uuid_, status, errors=errors)

        assert_that(event, equal_to(expected))


class TestPluginUninstallProgressEvent(TestCase):

    def test_marshal(self):
        uuid_ = new_uuid()
        status = 'start'

        event = PluginUninstallProgressEvent(uuid_, status)

        result = event.marshal()
        expected = {'uuid': uuid_, 'status': status}

        assert_that(result, equal_to(expected))

    def test_marshal_on_error(self):
        uuid_ = new_uuid()
        status = 'error'
        errors = {
            'error_id': 'packaging-error',
            'message': 'Packaging Error',
            'resource': 'plugins',
            'details': {},
        }

        event = PluginUninstallProgressEvent(uuid_, status, errors=errors)

        result = event.marshal()
        expected = {'uuid': uuid_, 'status': status, 'errors': errors}

        assert_that(result, equal_to(expected))

    def test_unmarshal(self):
        uuid_ = new_uuid()
        status = 'deleting'

        body = {'uuid': uuid_, 'status': status}
        event = PluginUninstallProgressEvent.unmarshal(body)
        expected = PluginUninstallProgressEvent(uuid_, status)

        assert_that(event, equal_to(expected))

    def test_unmarshal_on_error(self):
        uuid_ = new_uuid()
        status = 'building'
        errors = {
            'error_id': 'packaging-error',
            'message': 'Packaging Error',
            'resource': 'plugins',
            'details': {},
        }

        body = {'uuid': uuid_, 'status': status, 'errors': errors}
        event = PluginUninstallProgressEvent.unmarshal(body)
        expected = PluginUninstallProgressEvent(uuid_, status, errors=errors)

        assert_that(event, equal_to(expected))
