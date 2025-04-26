"""
File        : mkdocs_table_of_figures/constants.py
Description : Theses are some constants defined in setup.cfg
Author      : Thibaud Briard - BRT, <thibaud.briard@outlook.com>
"""

from configparser import ConfigParser
from pathlib import Path

config = ConfigParser()
config.read(Path(__file__).parent.parent / "setup.cfg")

PACKAGE_NAME = config["metadata"]["name"]
VERSION = config["metadata"]["version"]

# Parse entrypoint identifier
MKDOCS_ENTRYPOINT = config["options.entry_points"]["mkdocs.plugins"].split("=")[0].strip()
