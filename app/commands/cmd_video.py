import requests_cache
import datetime
import click
import logging

from app import app
from app import cli as app_cli
from app.amazon_browser import AmazonBrowser

log = logging.getLogger(__name__)

app = app.App()
today = datetime.datetime.today()

#####################################################################
# Settings

# cache settings
days_to_cache = 1

#####################################################################
# Click Code


@click.group()
def cli():
    """Subcommand for video"""

    pass


@cli.command()
@app_cli.pass_context
def clear_history(ctx):
    """This command loads config.yaml and the current ENV-ironment,
    creates a single merged dict, and prints to stdout.
    """

    # use cache to reduce web traffic
    requests_cache.CachedSession(
        cache_name='cache',
        backend='sqlite',
        expire_after=datetime.timedelta(days=days_to_cache))

    ab = AmazonBrowser()
    ab.login()
    ab.video_clear_history()


#####################################################################
# Functions
