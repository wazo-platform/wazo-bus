# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import subprocess
from tempfile import TemporaryDirectory
from unittest import TestCase

from wazo_test_helpers.asset_launching_test_case import (
    AbstractAssetLaunchingHelper,
    _run_cmd,
)


class DockerError(Exception):
    pass


class ValidationError(Exception):
    pass


class TestDocumentation(AbstractAssetLaunchingHelper, TestCase):
    asset = 'documentation'
    assets_root = os.path.join(os.path.dirname(__file__), '..', 'assets')
    service = 'spec-generator'
    validator = 'spec-validator'

    @classmethod
    def _generate_specfiles(
        cls, output_directory: os.PathLike
    ) -> subprocess.CompletedProcess:
        program: list[str] = ['docker-compose']
        options: list[str] = cls._docker_compose_options()
        args: list[str] = [
            'run',
            '-v',
            f'{output_directory}:/app/output',
            cls.service,
            '-p',
            'test-version',
        ]

        return _run_cmd(program + options + args)

    @classmethod
    def _validate_specfile(
        cls, name: str, path: os.PathLike
    ) -> subprocess.CompletedProcess:
        program: list[str] = ['docker-compose']
        options: list[str] = cls._docker_compose_options()
        args: list[str] = [
            'run',
            '-v',
            f'{path}:/{name}.yml',
            cls.validator,
            'validate',
            f'/{name}.yml',
        ]

        return _run_cmd(program + options + args)

    @classmethod
    def _has_errors(cls, process: subprocess.CompletedProcess) -> bool:
        output = process.stdout.decode().strip().split('\n')

        if '0 errors' not in output[-1]:
            return True
        return False

    def test_documentation_is_valid(self):
        with TemporaryDirectory() as basepath:
            result = self._generate_specfiles(basepath)
            if result.returncode != 0:
                print(result.stdout.decode())
                raise DockerError(
                    "An error occured while generating specification files"
                )

            for filename in os.listdir(basepath):
                path = os.path.join(basepath, filename)
                name, extension = os.path.splitext(filename)
                if extension.endswith('yml'):
                    result = self._validate_specfile(name, path)
                    result.check_returncode()

                    if self._has_errors(result):
                        print(result.stdout.decode())
                        raise ValidationError(
                            f'An error occured while validating {name} specification file'
                        )
