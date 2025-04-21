#!/usr/bin/env python3
"""
A cross-platform CLI tool for fetching images and Lucide icons,
and cleaning up unused Lucide icons in a target folder.

Usage (shell-escape from LaTeX):
  \write18{pyfetch fetch https://example.com/image.png --dest=images}
  \write18{pyfetch fetch-lucide a-arrow-down --dest=icons}
  \write18{pyfetch clean-lucide arrow-down,chevron-up --dest=icons}
  \write18{pyfetch update-color #FF0000 arrow-down,chevron-up --dest=icons}

Dependencies:
  - Python 3.7+
  - click
  - requests

Install:
  pip install click requests
"""
import sys
import logging
from pathlib import Path
import requests
import click

# Configure logging
def configure_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

# Base URL for raw Lucide icons
LUCIDE_RAW_BASE = "https://raw.githubusercontent.com/lucide-icons/lucide/main/icons"

@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose (debug) output')
@click.pass_context
def cli(ctx, verbose):
    """lucide-cli: A tool to fetch images and manage Lucide icons."""
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose
    configure_logging(verbose)

@cli.command()
@click.argument('url')
@click.option('-d', '--dest', 'dest_folder', default='.', type=click.Path(file_okay=False), help='Destination folder')
@click.pass_context
def fetch(ctx, url, dest_folder):
    """Fetch an image from a URL and save it into DEST folder."""
    dest = Path(dest_folder)
    dest.mkdir(parents=True, exist_ok=True)
    filename = Path(url).name or 'download'
    out_path = dest / filename
    logging.info(f"Fetching {url} -> {out_path}")
    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        with open(out_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info("Download complete")
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        sys.exit(1)

@cli.command('fetch-lucide')
@click.argument('icon_name')
@click.option('-d', '--dest', 'dest_folder', default='.', type=click.Path(file_okay=False), help='Destination folder')
@click.pass_context
def fetch_lucide(ctx, icon_name, dest_folder):
    """Fetch a Lucide SVG icon by name (without .svg) into DEST folder."""
    dest = Path(dest_folder)
    dest.mkdir(parents=True, exist_ok=True)
    resource = f"{icon_name}.svg"
    url = f"{LUCIDE_RAW_BASE}/{resource}"
    out_path = dest / resource
    logging.info(f"Fetching Lucide icon {icon_name} -> {out_path}")
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(out_path, 'wb') as f:
            f.write(resp.content)
        logging.info("Icon downloaded")
    except Exception as e:
        logging.error(f"Failed to fetch Lucide icon '{icon_name}': {e}")
        sys.exit(1)

@cli.command('clean-lucide')
@click.argument('icons')
@click.option('-d', '--dest', 'dest_folder', default='.', type=click.Path(file_okay=False), help='Target folder to clean')
@click.pass_context
def clean_lucide(ctx, icons, dest_folder):
    """Remove Lucide icons not listed in comma-separated ICONS from DEST folder."""
    dest = Path(dest_folder)
    if not dest.exists() or not dest.is_dir():
        logging.error(f"Destination folder does not exist: {dest}")
        sys.exit(1)
    keep = set(name.strip() for name in icons.split(','))
    removed = []
    for file in dest.iterdir():
        if file.is_file() and file.suffix == '.svg':
            name = file.stem
            if name not in keep:
                try:
                    file.unlink()
                    removed.append(name)
                    logging.info(f"Removed unused icon: {name}")
                except Exception as e:
                    logging.error(f"Failed to remove {file}: {e}")
    if not removed:
        logging.info("No unused icons found to remove.")
    else:
        logging.info(f"Cleaned {len(removed)} icons.")

if __name__ == '__main__':
    cli()
