from _typeshed import Incomplete
from datetime import datetime
from fsspec import AbstractFileSystem as AbstractFileSystem
from tlc.core.url import Scheme as Scheme, Url as Url
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry
from tlc.core.url_adapters.fsspec_url_adapter import FSSpecUrlAdapter as FSSpecUrlAdapter, FSSpecUrlAdapterDirEntry as FSSpecUrlAdapterDirEntry
from typing import Any

class GSUrlAdapterDirEntry(FSSpecUrlAdapterDirEntry):
    """A directory entry for a GSUrlAdapter"""
    def __init__(self, ls_info: dict[str, Any]) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def path(self) -> str: ...
    def mtime(self) -> datetime: ...

class GCSUrlAdapter(FSSpecUrlAdapter):
    """
    An adapter for resolving reads/writes to URLs starting with `gs://`
    """
    gs_scheme: Incomplete
    gs_protocol: Incomplete
    def schemes(self) -> list[Scheme]: ...
    def is_file_hierarchy_flat(self) -> bool: ...
    def touch(self, url: Url) -> None:
        """Update the last modified timestamp of a file to the current time.
        Creates the file if it doesn't exist.

        :param url: The URL of the file to touch
        """

logger: Incomplete
