"""
Initialize the application.
"""
import appdirs
import click
import click_log
import datetime
import logging
import os

APP_NAME = "blockout"
APP_AUTHOR = "datashaman"
DIRS = appdirs.AppDirs(APP_NAME, APP_AUTHOR)

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


def date_handler(obj):
    "Date handler for JSON serialization"
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
        return obj.isoformat()
    else:
        return None


def find_config(verbose=False):
    "Search for config on wellknown paths"
    search_paths = [
        os.path.join(os.getcwd(), "config.py"),
        os.path.join(DIRS.user_data_dir, "config.py"),
        os.path.join(DIRS.site_data_dir, "config.py"),
    ]

    config = None

    for search_path in search_paths:
        message = "Searching %s" % search_path
        logger.debug(message)
        if verbose:
            click.echo(message)

        if os.path.exists(search_path) and not os.path.isdir(search_path):
            config = search_path
            break

    return config


def echo(level, message):
    log_func = getattr(logger, level)
    log_func(message)
    click.echo(message)
