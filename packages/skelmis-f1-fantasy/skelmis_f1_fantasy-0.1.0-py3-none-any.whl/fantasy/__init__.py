import logging
from collections import namedtuple

from .client import Client

__version__ = "0.1.0"
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(
    major=0, minor=1, micro=0, releaselevel="pre-alpha", serial=0
)
logging.getLogger(__name__).addHandler(logging.NullHandler())
