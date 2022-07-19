import importlib
import inspect
import os
import yaml

from glob import glob
from concurrent.futures import ThreadPoolExecutor
from collections import ChainMap
from xivo_bus.resources.common.abstract import AbstractEvent

# from xivo_bus.resources.common.event import TenantEvent, UserEvent


RESOURCES_DIR = os.path.join("resources", "**", "event*.pyi")
KEYS_IGNORE_LIST = (
    'self',
    'tenant_uuid',
    'user_uuid',
)


def generate_format():
    spec = {
        'asyncapi': '2.0.0',
        'info': {
            'title': '',
            'version': '0.0.1',
        },
        'servers': {
            'production': {
                'url': 'amqp://guest:guest@localhost:5672/',
                'protocol': 'amqp',
                'protocolVersion': '0.9.1',
            }
        },
        'channels': {},
        'components': {
            'messages': {},
            'schemas': {
                'tenant_uuid': {
                    'type': 'string',
                    'format': 'uuid',
                    'description': 'Resource\'s associated tenant\'s UUID',
                },
                'user_uuid': {
                    'name': 'user_uuid',
                    'type': 'boolean',
                    'description': 'Targeted user\'s uuid.  The format user_uuid:<uuid> allows '
                    'multiple users to be the recipient of the event',
                },
            },
        },
    }
    return spec


def generate_event_headers(cls, keys):
    headers = {
        'name': {
            'type': 'string',
            'const': cls.name,
        }
    }

    if 'tenant_uuid' in keys:
        headers['tenant_uuid'] = {'$ref': '#/components/schemas/tenant_uuid'}
    if 'user_uuid' in keys:
        headers['user_uuid:{uuid}'] = {'$ref': '#/components/schemas/user_uuid'}
    return headers


def generate_event_payload(cls):
    try:
        yml = yaml.safe_load(cls.__doc__)
    except AttributeError:
        return {}

    return {'data': yml['payload']}


def generate_event_spec(cls):
    fn_sig = inspect.signature(cls.__init__)
    fn_args = fn_sig.parameters.keys()

    try:
        doc = yaml.safe_load(cls.__doc__)
    except AttributeError:
        doc = {}

    headers = generate_event_headers(cls, fn_args)
    payload = generate_event_payload(cls)

    event_spec = {
        'subscribe': {
            'summary': doc.get('summary', ''),
            'message': {
                'payload': {
                    'type': 'object',
                    'properties': payload,
                },
                'headers': {
                    'type': 'object',
                    'properties': headers,
                },
            },
        }
    }
    return event_spec


def get_event_spec(path):
    module_name = os.path.splitext(path)[0].replace('/', '.')
    spec = {}

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return {}

    for item in dir(module):
        if item.startswith('__'):
            continue

        cls = getattr(module, item)
        if not isinstance(cls, type) or inspect.isabstract(cls):
            continue

        if not issubclass(cls, AbstractEvent):
            continue

        spec[cls.name] = generate_event_spec(cls)
    return spec


def import_events(base_cls=None):
    resources_dir = os.path.join("resources", "**", "event*.py")

    paths = glob(resources_dir, recursive=False)
    spec = generate_format()

    with ThreadPoolExecutor() as executor:
        results = executor.map(get_event_spec, paths)

    spec['channels'] = dict(ChainMap(*[result for result in results]))

    with open('events_spec.yml', 'w') as file:
        yaml.dump(spec, file, sort_keys=False)
