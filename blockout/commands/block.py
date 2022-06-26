"""
Command for blocking a user on Twitter
"""

import json

import click

from blockout.cli import cli
from blockout.twitter import get_access_token, get_session, verify_credentials

@cli.command()
@click.argument('id')
@click.pass_context
def block(ctx, id):
    "Block user on Twitter"
    access_token = get_access_token(ctx, False)
    session = get_session(ctx, access_token)
    credentials = verify_credentials(session)

    response = session.post("https://api.twitter.com/2/users/{}/blocking".format(credentials['id']), json={
        "target_user_id": id,
    })

    if response.status_code == 403:
        contents = response.json()
        click.echo(json.dumps(contents, indent=4, sort_keys=True))
