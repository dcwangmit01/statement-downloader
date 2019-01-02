import requests_cache
import datetime
import click
import logging

from app import app
from app import cli as app_cli
from app.schwab import Schwab

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
    """Subcommand for schwab"""

    pass


@cli.command(name='all')
@click.argument('download-dir', type=click.Path(exists=True))
@click.argument('save-dir', type=click.Path(exists=True))
@app_cli.pass_context
def _all(ctx, download_dir, save_dir):
    """Downloads all schwab statements"""

    # use cache to reduce web traffic
    requests_cache.CachedSession(
        cache_name='cache', backend='sqlite', expire_after=datetime.timedelta(days=days_to_cache))

    s = Schwab(download_dir, save_dir)
    s.login()
    s.download_all()


#####################################################################
# Functions
