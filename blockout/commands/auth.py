"""
Command for authorizing the application in the user's account.
"""

from blockout.cli import cli
from blockout.twitter import get_access_token

@cli.command()
@click.pass_context
def authorize(ctx):
    access_token = get_access_token(ctx, False)
    click.echo(json.dumps(access_token, indent=4))
