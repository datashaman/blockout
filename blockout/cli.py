#!/usr/bin/env python
"""
CLI entry module.
"""

import click
import click_log
import importlib.util
import logging

from . import find_config

logger = logging.getLogger(__name__)

config = None
config_file = find_config()

if config_file:
    spec = importlib.util.spec_from_file_location("config", config_file)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)


@click.group()
@click_log.simple_verbosity_option(logger)
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)

    logger.info("Started")


from . import commands


def main():
    cli(auto_envvar_prefix="BLOCKOUT", obj={})
