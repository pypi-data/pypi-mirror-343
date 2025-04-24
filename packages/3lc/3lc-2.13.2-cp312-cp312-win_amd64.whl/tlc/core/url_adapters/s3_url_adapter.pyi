from _typeshed import Incomplete
from datetime import datetime
from fsspec import AbstractFileSystem as AbstractFileSystem
from tlc.core.url import Scheme as Scheme, Url as Url
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry
from tlc.core.url_adapters.fsspec_url_adapter import FSSpecUrlAdapter as FSSpecUrlAdapter, FSSpecUrlAdapterDirEntry as FSSpecUrlAdapterDirEntry
from typing import Any

logger: Incomplete

class S3UrlAdapterDirEntry(FSSpecUrlAdapterDirEntry):
    """A directory entry for an S3UrlAdapter"""
    def __init__(self, ls_info: dict[str, Any]) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def path(self) -> str: ...
    def mtime(self) -> datetime:
        """Get the last modification time of the file.

        :raises: AttributeError if the modification time is not available
        :returns: The modification time as a datetime
        """

class S3UrlAdapter(FSSpecUrlAdapter):
    """
    An adapter for resolving reads/writes to URLs starting with `s3://`
    """
    s3_scheme: Incomplete
    s3_protocol: Incomplete
    def __init__(self) -> None: ...
    def schemes(self) -> list[Scheme]: ...
    def is_file_hierarchy_flat(self) -> bool: ...
    def touch(self, url: Url) -> None:
        """Update the last modified timestamp of a file to the current time.
        Creates the file if it doesn't exist.

        :param url: The URL of the file to touch
        """
    def read_string_content_from_url(self, url: Url) -> str:
        """Read the content of a file as a string.

        This function overrides the FSSpecUrlAdapter base class implementation which uses `read_text()`. We use
        `read_bytes().decode()` instead since `S3FileSystem.read_text()` makes an unnecessary and expensive
        `head_object` API call to S3.

        :param url: The URL of the file to read
        :returns: The content of the file as a string
        """
