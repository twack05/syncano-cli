# -*- coding: utf-8 -*-
import os

from syncano_cli.config import ACCOUNT_CONFIG, ACCOUNT_CONFIG_PATH
from syncano_cli.main import cli
from tests.base import InstanceMixin, IntegrationTest


class SyncCommandsTest(InstanceMixin, IntegrationTest):

    def test_login(self):
        self.runner.invoke(cli, args=['login'], obj={}, input='{email}\n{password}\n'.format(
            email=self.API_EMAIL,
            password=self.API_PASSWORD
        ))
        self.assertTrue(ACCOUNT_CONFIG.get('DEFAULT', 'key'))
        self.assertTrue(os.path.isfile(ACCOUNT_CONFIG_PATH))

    def test_sync_push(self):
        result = self.runner.invoke(cli, args=[
            'sync', 'push', 'test',
            '--class', 'test_class',
            '--scripts', 'test_script',
            '--all',
        ], obj={})
        self.assertIn('', result.output)

    def test_sync_pull(self):
        result = self.runner.invoke(cli, args=[
            'sync', 'pull', 'test',
            '--class', 'test_class',
            '--scripts', 'test_script',
            '--all',
        ], obj={})
        self.assertIn('', result.output)

    def test_watch(self):
        result = self.runner.invoke(cli, args=['sync', 'watch', 'test'], obj={})
        self.assertIn('', result.output)
