"""
Command for blocking a user on Twitter
"""

import json

import click

from blockout.cli import cli
from blockout.twitter import get_twitter

@cli.command()
@click.argument('id')
@click.pass_context
def block(ctx, id):
    "Block user on Twitter"
    twitter = get_twitter(ctx)
    click.echo(twitter.blocks.list())
