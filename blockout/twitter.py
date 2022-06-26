import json
import os

import appdirs
import click

from blockout.constants import APP_AUTHOR, APP_NAME
from requests_oauthlib import OAuth1Session


def verify_credentials(session):
    return session.get("https://api.twitter.com/1.1/account/verify_credentials.json").json()


def authenticate(session):
    authorization_url = session.authorization_url("https://api.twitter.com/oauth/authenticate")
    click.echo(authorization_url)

    click.echo("Please go here and authorize: %s" % authorization_url)

    return input("Paste the PIN here: ")


def authorize(session):
    authorization_url = session.authorization_url("https://api.twitter.com/oauth/authorize")
    click.echo("Please go here and authorize: %s" % authorization_url)

    return input("Paste the PIN here: ")


def get_access_token_path(ctx):
    user_cache_dir = appdirs.user_cache_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(user_cache_dir, mode=0o700, exist_ok=True)
    return os.path.join(user_cache_dir, 'token.txt')


def create_access_token(ctx):
    session = OAuth1Session(ctx.obj['KEY'], client_secret=ctx.obj['SECRET'])
    resource_owner_token = session.fetch_request_token("https://api.twitter.com/oauth/request_token")

    session = OAuth1Session(
        ctx.obj['KEY'],
        client_secret=ctx.obj['SECRET'],
        resource_owner_key=resource_owner_token['oauth_token'],
        resource_owner_secret=resource_owner_token['oauth_token_secret'],
        verifier=authenticate(session),
    )

    access_token = session.fetch_access_token("https://api.twitter.com/oauth/access_token")

    with open(get_access_token_path(ctx), 'w') as access_token_file:
        contents = json.dumps(access_token, indent=4)
        access_token_file.write(contents)

    return access_token


def get_access_token(ctx, use_existing=True):
    if not use_existing:
        return create_access_token(ctx)

    access_token = None

    try:
        with open(get_access_token_path(ctx), 'r') as access_token_file:
            contents = access_token_file.read()
            access_token = json.loads(contents)
    except FileNotFoundError:
        access_token = create_access_token(ctx)

    return access_token


def get_session(ctx, access_token=None):
    if access_token is None:
        access_token = get_access_token(ctx)

    return OAuth1Session(
        ctx.obj['KEY'],
        client_secret=ctx.obj['SECRET'],
        resource_owner_key=access_token['oauth_token'],
        resource_owner_secret=access_token['oauth_token_secret'],
    )
