# Copyright 2022-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import argparse
import importlib
import inspect
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from itertools import chain
from pathlib import Path
from sys import stdout
from time import time
from types import UnionType
from typing import (
    Annotated,
    Any,
    Callable,
    Literal,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    is_typeddict,
)

import yaml
from typing_extensions import TypeAlias

PACKAGE_NAME = 'xivo_bus'

logging.basicConfig(stream=stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AsyncAPITypes:
    class Types:
        @classmethod
        def array(cls, format: dict[str, str]) -> dict:
            return {'type': 'array', 'items': format}

        @classmethod
        def boolean(cls, *metadata: Any) -> dict:
            return {'type': 'boolean'}

        @classmethod
        def float_(cls, *metadata: Any) -> dict:
            return {'type': 'float'}

        @classmethod
        def integer(cls, *metadata: Any) -> dict:
            return {'type': 'integer'}

        @classmethod
        def object_(cls, content: dict | None = None, *metadata: Any) -> dict:
            return {'type': 'object', 'properties': content or {}}

        @classmethod
        def string(cls, *metadata: Any) -> dict:
            content = {'type': 'string'}

            for obj in metadata:
                print(obj)
                if hasattr(obj, 'format'):
                    content['format'] = obj.format

                if hasattr(obj, 'const'):
                    content['const'] = obj.const

            return content

    _TYPES_FACTORIES: dict[type | Any, Callable[..., dict]] = {
        Any: Types.object_,
        bool: Types.boolean,
        dict: Types.object_,
        float: Types.float_,
        int: Types.integer,
        str: Types.string,
    }

    @classmethod
    def _scan_hint(cls, hint: type) -> dict[str, str]:
        def recurse(type_: type, *metadata: Any) -> dict:
            if origin_type := get_origin(type_):
                subtype, *args = get_args(type_)

                if origin_type is Annotated:
                    return recurse(subtype, *args)

                elif origin_type is Literal:
                    return cls.Types.string(*args)

                elif origin_type in (UnionType, Union):
                    return recurse(subtype)

                elif origin_type in (list, set, tuple):
                    if len(args) > 0:
                        raise TypeError('arrays cannot have multiple types')
                    return cls.Types.array(recurse(subtype))

                elif origin_type is dict:
                    return cls.Types.object_()

            elif is_typeddict(type_):
                content = {
                    name: recurse(subtype)
                    for name, subtype in get_type_hints(
                        type_, include_extras=True
                    ).items()
                }
                return cls.Types.object_(content)

            elif type_ in cls._TYPES_FACTORIES.keys():
                factory = cls._TYPES_FACTORIES[type_]
                return factory(*metadata)

            raise TypeError(f'unhandled type: {type_}')

        return recurse(hint)

    @classmethod
    def from_init(cls, class_: type, *, ignore_keys: set[str] | None = None) -> dict:
        ignore_keys = ignore_keys or set()
        init_fn = getattr(class_, '__init__')

        hints: dict[str, type] = {
            param: type_
            for param, type_ in get_type_hints(init_fn, include_extras=True).items()
            if param not in ignore_keys
        }

        return {param: cls._scan_hint(hint) for param, hint in hints.items()}


class Event:
    _DEFAULT_PAYLOAD_IGNORE_KEYS = {
        'self',
        'return',
        'tenant_uuid',
        'user_uuid',
        'user_uuids',
    }

    def __init__(self, class_: type):
        self.class_ = class_
        sig = inspect.signature(getattr(class_, '__init__'))
        self._parameters = sig.parameters
        self._keys = sig.parameters.keys()

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.class_, attr)

    def __lt__(self, other: TypeAlias) -> bool:
        return self.name < other.name

    @staticmethod
    def is_event(class_: type) -> bool:
        if not inspect.isclass(class_):
            return False

        if not all(
            hasattr(class_, attr) for attr in ('name', 'routing_key_fmt', 'content')
        ):
            return False

        if inspect.isabstract(class_):
            return False

        return True

    def __repr__(self) -> str:
        return f'<Event \'{self.name}\'>'

    @property
    def service(self) -> str:
        return getattr(self.class_, 'service', 'undefined')

    def generate_tag(self) -> list[dict]:
        return [{'name': self.service}]

    def generate_headers(self) -> dict:
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

        if any([key in self._keys for key in ('user_uuid', 'user_uuids')]):
            headers['user_uuid:{uuid}'] = {
                '$ref': '#/components/schemas/user_uuid:{uuid}'
            }
            required.append('user_uuid:{uuid}')

        return {'type': 'object', 'properties': headers, 'required': required}

    def generate_payload(self) -> dict:
        return AsyncAPITypes.from_init(
            self.class_, ignore_keys=self._DEFAULT_PAYLOAD_IGNORE_KEYS
        )

    def generate_parameters(self) -> dict:
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

    def generate_specification(self) -> dict:
        message_name = '-'.join([self.name.replace('_', '-'), 'payload'])
        doc = yaml.safe_load(self.class_.__doc__ or '')

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
    def __init__(self, input_schema: str, version: str):
        self.platform_version = str(version)
        self.base_path = self.get_package_path(PACKAGE_NAME)
        resource_dir = self.base_path.joinpath('resources')
        self.paths = [path for path in resource_dir.iterdir() if path.is_dir()]

        with open(input_schema) as file:
            self.input_schema = yaml.safe_load(file)

    @staticmethod
    def get_package_path(package_name: str) -> Path:
        module = importlib.import_module(package_name)
        entrypoint = inspect.getfile(module)
        return Path(os.path.dirname(entrypoint))

    def get_resource_events(self, resource_path: Path) -> list[Event]:
        events: list[Event] = []
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

    def generate_specifications(self, events: list[Event]) -> dict:
        print(
            f'generating AsyncAPI specifications for `{self.platform_version}` '
            f'({len(events)} events)'
        )
        specifications: dict = {}
        for event in events:
            service = event.service
            if service not in specifications:
                specifications[service] = {}
            specifications[service].update(event.generate_specification())
            print('.', end='')
        print('\n')
        return specifications

    def write_specifications(
        self, specifications: dict, output_dir: str, *, dry_run: bool = False
    ) -> None:
        def write(service: str) -> str:
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

    def run(self, output_dir: str = 'asyncapi', *, dry_run: bool = False) -> None:
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


def generate_documentation(
    template_file: str, output_dir: str, version: str, *, dry_run: bool = False
) -> None:
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
