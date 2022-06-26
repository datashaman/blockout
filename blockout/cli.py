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
@click.option('--key', help='Twitter consumer key')
@click.password_option('--secret', help='Twitter consumer secret')
@click.password_option('--token', help='Twitter bearer token')
@click.password_option('--user_id', help='Twitter user ID')
@click.pass_context
def cli(ctx, key, secret, token, user_id):
    ctx.ensure_object(dict)

    ctx.obj['KEY'] = key
    ctx.obj['SECRET'] = secret
    ctx.obj['TOKEN'] = token
    ctx.obj['USER_ID'] = user_id

    logger.info("Started")


from blockout import commands


def main():
    cli(auto_envvar_prefix="BLOCKOUT", obj={})
