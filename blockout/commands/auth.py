"""
Command for authorizing the application in the user's account.
"""

import click

from blockout.cli import cli
from blockout.twitter import get_twitter

@cli.command()
@click.pass_context
def auth(ctx):
    twitter = get_twitter(ctx)
    twitter.oauth.authorize(response_type='code', scope=[])
