import os
import sys
import logging

import click
from click import types

from syncanocli import __version__
from syncanocli import logger
from . import settings


OPTIONS_MAPPING = {
    'StringField': types.StringParamType,
    'IntegerField': types.IntParamType,
    'FloatField': types.FloatParamType,
    'BooleanField': types.BoolParamType,
    'SlugField': types.StringParamType,
    'EmailField': types.StringParamType,
    'ChoiceField': types.Choice,
    'DateField': types.StringParamType,
    'DateTimeField': types.StringParamType,
    'Field': types.StringParamType,
    'HyperlinkedField': types.StringParamType,
    'ModelField': types.StringParamType,
    'JSONField': types.StringParamType,
    'SchemaField': types.StringParamType,
}


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


def set_loglevel(ctx, param, value):
    value = value.upper()
    loglevel = getattr(logging, value, None)

    if not isinstance(loglevel, int):
        raise click.BadParameter('Invalid log level: {0}.'.format(loglevel))

    logger.setLevel(loglevel)
    return value


class AutodiscoverMultiCommand(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(settings.COMMANDS_FOLDER):
            if filename.endswith('.py') and not filename.startswith('_'):
                rv.append(filename[:-3])

        rv.extend(settings.ALIASES.keys())
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        command = 'cli'

        if name in settings.ALIASES:
            alias = settings.ALIASES[name]
            name, command = alias.rsplit('.', 1)
        
        try:
            module_name = 'syncanocli.commands.{0}'.format(name)
            module = __import__(module_name, None, None, [command])
        except ImportError:
            return

        logger.debug('Command loaded: {0}'.format(module))
        return getattr(module, command)
