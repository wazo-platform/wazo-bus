# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import importlib
import inspect
import logging
import os
import re
import yaml

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from itertools import chain
from pathlib import Path
from sys import stdout
from time import time

from xivo_bus.resources.common.abstract import AbstractEvent


PACKAGE_NAME = 'xivo_bus'

logging.basicConfig(stream=stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AsyncAPITypes:
    @staticmethod
    def string(*, many=False):
        fmt = {'type': 'string'}
        return AsyncAPITypes.array(fmt) if many else fmt

    @staticmethod
    def boolean(*, many=False):
        fmt = {'type': 'boolean'}
        return AsyncAPITypes.array(fmt) if many else fmt

    @staticmethod
    def integer(*, many=False):
        fmt = {'type': 'integer'}
        return AsyncAPITypes.array(fmt) if many else fmt

    @staticmethod
    def float_(*, many=False):
        fmt = {'type': 'float'}
        return AsyncAPITypes.array(fmt) if many else fmt

    @staticmethod
    def uuid(*, many=False):
        fmt = {'type': 'string', 'format': 'uuid'}
        return AsyncAPITypes.array(fmt) if many else fmt

    @staticmethod
    def datetime(*, many=False):
        fmt = {'type': 'string', 'format': 'date-time'}
        return AsyncAPITypes.array(fmt) if many else fmt

    @staticmethod
    def array(type_):
        return {'type': 'array', 'items': type_}

    @staticmethod
    def object_(dict_=None):
        return {'type': 'object', 'properties': dict_ or {}}


class Event:
    def __init__(self, class_):
        self.class_ = class_

        sig = inspect.signature(class_.__init__)
        self._keys = sig.parameters.keys()

    def __getattr__(self, attr):
        return getattr(self.class_, attr)

    def __lt__(self, other):
        return self.name < other.name

    @staticmethod
    def is_event(class_):
        if not inspect.isclass(class_):
            return False

        if not issubclass(class_, AbstractEvent):
            return False

        if inspect.isabstract(class_):
            return False

        return True

    def __repr__(self):
        return f'<Event \'{self.name}\'>'

    @property
    def service(self):
        return getattr(self.class_, 'service', 'undefined')

    def generate_tag(self):
        return [{'name': self.service}]

    def generate_headers(self):
        headers = {
            'name': {
                'type': 'string',
                'const': self.name,
                'description': 'Name of the event (used for routing the message)',
            },
            'required_access': {
                'type': 'string',
                'const': f'event.{self.name}',
                'description': 'Necessary user access required to read this event',
            },
            'origin_uuid': {'$ref': '#/components/schemas/origin_uuid'},
            'timestamp': {'$ref': '#/components/schemas/timestamp'},
        }
        required = ['name', 'required_access', 'origin_uuid', 'timestamp']

        if 'tenant_uuid' in self._keys:
            headers['tenant_uuid'] = {'$ref': '#/components/schemas/tenant_uuid'}
            required.append('tenant_uuid')

        if 'user_uuid' in self._keys:
            headers['user_uuid:{uuid}'] = {
                '$ref': '#/components/schemas/user_uuid:{uuid}'
            }
            required.append('user_uuid:{uuid}')

        return {'type': 'object', 'properties': headers, 'required': required}

    def generate_payload(self):
        content = {}
        keys_ignore_list = ('tenant_uuid', 'user_uuid', 'self')
        content_keys = [key for key in self._keys if key not in keys_ignore_list]

        for key in content_keys:
            if key.endswith('uuid'):
                content[key] = AsyncAPITypes.uuid()
            elif key.endswith('uuids'):
                content[key] = AsyncAPITypes.uuid(many=True)
            elif key.endswith(('id', 'number')):
                content[key] = AsyncAPITypes.integer()
            elif key.startswith('is_'):
                content[key] = AsyncAPITypes.boolean()
            elif key.endswith('_at'):
                content[key] = AsyncAPITypes.datetime()
            elif key.endswith(('_data', '_info', '_schema')):
                content[key] = AsyncAPITypes.object_()
            else:
                content[key] = AsyncAPITypes.string()

        return AsyncAPITypes.object_(
            dict(data=AsyncAPITypes.object_(content)),
        )

    def generate_parameters(self):
        parameters = {}
        matches = re.search(r'\{(.*?)\}', self.name)
        if matches:
            for param in matches.groups() or []:
                parameters[param] = {
                    'description': '',
                    'schema': {
                        'type': 'string',
                    },
                }
        return parameters

    def generate_specification(self):
        message_name = '-'.join([self.name.replace('_', '-'), 'payload'])

        try:
            doc = yaml.safe_load(self.class_.__doc__)
        except AttributeError:
            doc = ''

        spec = {
            'subscribe': {
                'summary': doc or '',
                'tags': self.generate_tag(),
                'message': {
                    'name': message_name,
                    'payload': self.generate_payload(),
                    'headers': self.generate_headers(),
                },
            }
        }

        parameters = self.generate_parameters()
        if parameters:
            spec['parameters'] = parameters

        return {self.name: spec}


class EventSpecificationBuilder:
    def __init__(self, input_schema, version):
        self.platform_version = str(version)
        self.base_path = self.get_package_path(PACKAGE_NAME)
        resource_dir = self.base_path.joinpath('resources')
        self.paths = [path for path in resource_dir.iterdir() if path.is_dir()]

        with open(input_schema) as file:
            self.input_schema = yaml.safe_load(file)

    @staticmethod
    def get_package_path(package_name):
        module = importlib.import_module(package_name)
        entrypoint = inspect.getfile(module)
        return Path(os.path.dirname(entrypoint))

    def get_resource_events(self, resource_path):
        events = []
        file_paths = sorted(resource_path.glob('*.py'))

        for path in file_paths:
            name = os.path.splitext(path.relative_to(self.base_path))[0]
            import_name = '.'.join([PACKAGE_NAME, name.replace('/', '.')])

            try:
                module = importlib.import_module(import_name)
            except ModuleNotFoundError as e:
                print(f'skipping {name}: {e}')
                continue

            events.extend(
                Event(cls) for _, cls in inspect.getmembers(module, Event.is_event)
            )

        return events

    def generate_specifications(self, events):
        print(
            f'generating AsyncAPI specifications for `{self.platform_version}` ({len(events)} events)'
        )
        specifications = {}
        for event in events:
            service = event.service
            if service not in specifications:
                specifications[service] = {}
            specifications[service].update(event.generate_specification())
            print('.', end='')
        print('\n')
        return specifications

    def write_specifications(self, specifications, output_dir, *, dry_run=False):
        def write(service):
            service_name = (
                '-'.join(['wazo', service]) if service != 'undefined' else service
            )
            path = Path(output_dir).joinpath(f'{service_name}.yml').resolve()
            schema = deepcopy(self.input_schema)
            schema['info']['title'] = f'{service_name} events'
            schema['info']['version'] = self.platform_version
            schema['channels'] = specifications[service]

            if dry_run:
                return f'would write \'{path}\''

            with open(path, 'w') as file:
                yaml.dump(schema, file, sort_keys=False)
            size = path.stat().st_size / 1024
            return f'wrote \'{path}\' ({size:.2f} KB)'

        with ThreadPoolExecutor() as executor:
            futs = [
                executor.submit(write, service) for service in specifications.keys()
            ]
        [print(fut.result()) for fut in futs]

    def run(self, output_dir='asyncapi', *, dry_run=False):
        start_time = time()
        if dry_run:
            print('[DRY RUN]')

        with ThreadPoolExecutor() as executor:
            results = executor.map(self.get_resource_events, self.paths)

        events = sorted(chain(*results))
        specifications = self.generate_specifications(events)

        self.write_specifications(specifications, output_dir, dry_run=dry_run)
        exec_time = time() - start_time
        print(f'(execution took \'{exec_time:.3f}\' seconds)')


def generate_documentation(template_file, output_dir, version, *, dry_run=False):
    builder = EventSpecificationBuilder(template_file, version)
    builder.run(output_dir, dry_run=dry_run)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract AsyncAPI specification for service\'s events'
    )

    parser.add_argument('-o', type=str, dest='output_dir', required=True)
    parser.add_argument('-p', type=str, dest='platform_version', required=True)
    parser.add_argument(
        '-t', type=str, dest='template_file', default='asyncapi-template.yml'
    )
    parser.add_argument(
        '--dry', action='store_true', dest='dry_run', help='don\'t write files'
    )

    parsed = parser.parse_args()
    generate_documentation(
        parsed.template_file,
        parsed.output_dir,
        parsed.platform_version,
        dry_run=parsed.dry_run,
    )
