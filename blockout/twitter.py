import json
import os

import appdirs
import click

from blockout.constants import APP_AUTHOR, APP_NAME
from twitter import OAuth, oauth_dance, read_token_file, Twitter


def get_token_path(ctx):
    user_cache_dir = appdirs.user_cache_dir(APP_NAME, APP_AUTHOR)
    os.makedirs(user_cache_dir, mode=0o700, exist_ok=True)
    return os.path.join(user_cache_dir, 'token.txt')


def get_twitter(ctx):
    token_path = get_token_path(ctx)

    if not os.path.exists(token_path):
         oauth_dance(APP_NAME, ctx.obj['CONSUMER_KEY'], ctx.obj['CONSUMER_SECRET'], token_path)

    token, token_secret = read_token_file(token_path)

    return Twitter(auth=OAuth(token, token_secret, ctx.obj['CONSUMER_KEY'], ctx.obj['CONSUMER_SECRET']))
