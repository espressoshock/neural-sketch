#!/usr/bin/env python3
"""
A cross-platform CLI tool for fetching images and Lucide icons,
and cleaning up unused Lucide icons in a target folder.

Usage (shell-escape from LaTeX):
  \write18{pyfetch fetch https://example.com/image.png --dest=images}
  \write18{pyfetch fetch-lucide a-arrow-down --dest=icons}
  \write18{pyfetch clean-lucide arrow-down,chevron-up --intdir=icons/out --dest=icons}
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
import xml.etree.ElementTree as ET
import re


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
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose (debug) output")
@click.pass_context
def cli(ctx, verbose):
    """lucide-cli: A tool to fetch images and manage Lucide icons."""
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose
    configure_logging(verbose)


@cli.command()
@click.argument("url")
@click.option(
    "-d",
    "--dest",
    "dest_folder",
    default=".",
    type=click.Path(file_okay=False),
    help="Destination folder",
)
@click.pass_context
def fetch(ctx, url, dest_folder):
    """Fetch an image from a URL and save it into DEST folder."""
    dest = Path(dest_folder)
    dest.mkdir(parents=True, exist_ok=True)
    filename = Path(url).name or "download"
    out_path = dest / filename
    logging.info(f"Fetching {url} -> {out_path}")
    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        logging.info("Download complete")
    except Exception as e:
        logging.error(f"Failed to fetch {url}: {e}")
        sys.exit(1)


@cli.command("fetch-lucide")
@click.argument("icon_name")
@click.option(
    "-d",
    "--dest",
    "dest_folder",
    default=".",
    type=click.Path(file_okay=False),
    help="Destination folder",
)
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
        with open(out_path, "wb") as f:
            f.write(resp.content)
        logging.info("Icon downloaded")
    except Exception as e:
        logging.error(f"Failed to fetch Lucide icon '{icon_name}': {e}")
        sys.exit(1)


@cli.command("clean-lucide")
@click.argument("icons")
@click.option(
    "-i",
    "--intdir",
    "int_dir",
    required=True,
    type=click.Path(file_okay=False),
    help="Intermediate folder to clean",
)
@click.option(
    "-d",
    "--dest",
    "dest_folder",
    default=".",
    type=click.Path(file_okay=False),
    help="Folder of SVG icons to clean",
)
@click.pass_context
def clean_lucide(ctx, icons, int_dir, dest_folder):
    """Remove icons not in ICONS from DEST and related files in INTDIR."""
    dest = Path(dest_folder)
    int_dir = Path(int_dir)

    # Validate directories
    for path, name in ((dest, "dest"), (int_dir, "intdir")):
        if not path.exists() or not path.is_dir():
            logging.error(f"{name} folder does not exist or is not a directory: {path}")
            sys.exit(1)

    keep = set(name.strip() for name in icons.split(","))
    removed_icons = []

    # Clean DEST svg files
    for file in dest.iterdir():
        if file.is_file() and file.suffix == ".svg":
            stem = file.stem
            if stem not in keep:
                try:
                    file.unlink()
                    removed_icons.append(stem)
                    logging.info(f"Removed unused icon: {stem}")
                except Exception as e:
                    logging.error(f"Failed to remove {file}: {e}")
    if not removed_icons:
        logging.info("No unused SVG icons found to remove.")
    else:
        logging.info(f"Removed {len(removed_icons)} unused icons.")

    removed_int = []
    # Clean INTDIR files matching prefix_*.* where prefix not in keep
    prefix_re = re.compile(r"^([^_]+)_")
    for file in int_dir.iterdir():
        if file.is_file():
            m = prefix_re.match(file.name)
            if m:
                prefix = m.group(1)
                if prefix not in keep:
                    try:
                        file.unlink()
                        removed_int.append(file.name)
                        logging.info(f"Removed unused file in intdir: {file.name}")
                    except Exception as e:
                        logging.error(f"Failed to remove {file}: {e}")
    if not removed_int:
        logging.info("No unused intdir files found to remove.")
    else:
        logging.info(f"Removed {len(removed_int)} files from intdir.")


@cli.command("update-color")
@click.argument("color")
@click.argument("icons")
@click.option(
    "-d",
    "--dest",
    "dest_folder",
    default=".",
    type=click.Path(file_okay=False),
    help="Target folder containing SVGs",
)
@click.pass_context
def update_color(ctx, color, icons, dest_folder):
    """Update the SVG 'stroke' attribute to COLOR for listed Lucide icons only if different."""
    dest = Path(dest_folder)
    if not dest.exists() or not dest.is_dir():
        logging.error(f"Destination folder does not exist: {dest}")
        sys.exit(1)
    names = set(name.strip() for name in icons.split(","))
    updated = []
    for name in names:
        file_path = dest / f"{name}.svg"
        if not file_path.exists():
            logging.warning(f"Icon file not found, skipping: {file_path}")
            continue
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            changed = False
            for elem in root.iter():
                if "stroke" in elem.attrib and elem.attrib["stroke"] != color:
                    elem.set("stroke", color)
                    changed = True
            if changed:
                tree.write(file_path, encoding="utf-8", xml_declaration=True)
                updated.append(name)
                logging.info(f"Updated stroke color for: {name}")
            else:
                logging.info(f"{name}: stroke already set to {color}, skipping.")
        except Exception as e:
            logging.error(f"Failed to update {file_path}: {e}")
    if not updated:
        logging.info("No icons were updated.")
    else:
        logging.info(f"Updated color on {len(updated)} icons.")


if __name__ == "__main__":
    cli()
