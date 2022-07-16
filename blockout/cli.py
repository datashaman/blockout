#!/usr/bin/env python
"""
CLI entry module.
"""

import click
import click_log
import importlib.util
import logging

from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger)
@click.option('--consumer-key', help='Twitter consumer key')
@click.password_option('--consumer-secret', help='Twitter consumer secret')
@click.pass_context
def cli(ctx, consumer_key, consumer_secret):
    ctx.ensure_object(dict)

    ctx.obj['CONSUMER_KEY'] = consumer_key
    ctx.obj['CONSUMER_SECRET'] = consumer_secret

    logger.info("Started")


from blockout import commands


def main():
    cli(auto_envvar_prefix="BLOCKOUT", obj={})
