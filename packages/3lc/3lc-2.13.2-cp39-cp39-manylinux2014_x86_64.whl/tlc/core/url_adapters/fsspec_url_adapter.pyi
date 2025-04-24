import abc
from _typeshed import Incomplete
from abc import abstractmethod
from collections.abc import Iterator
from datetime import datetime
from fsspec import AbstractFileSystem as AbstractFileSystem
from tlc.core.url import Url as Url
from tlc.core.url_adapter import UrlAdapterAsyncFromSync as UrlAdapterAsyncFromSync, UrlAdapterDirEntry as UrlAdapterDirEntry
from typing import Any

logger: Incomplete

class FSSpecUrlAdapterDirEntry(UrlAdapterDirEntry, metaclass=abc.ABCMeta):
    """A directory entry for an FSSpecUrlAdapter"""
    def __init__(self, ls_info: dict[str, Any]) -> None: ...
    @property
    @abstractmethod
    def name(self) -> str: ...
    @property
    @abstractmethod
    def path(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def is_dir(self) -> bool: ...
    def is_file(self) -> bool: ...
    @abstractmethod
    def mtime(self) -> datetime: ...
    def mtime_datetime(self) -> datetime: ...

class FSSpecUrlAdapter(UrlAdapterAsyncFromSync, metaclass=abc.ABCMeta):
    """
    An adapter for resolving reads/writes to URLs using an implementation of fsspec.

    The basic workflow for each public method providing access to a URL is to translate the URL to a file system URL key
    that identifies the file system instance to use when accessing that URL, get or create a file system instance for
    that URL key, and then use that file system instance to access the URL.

    Translation of a URL to a file system URL key is done using _get_fs_url_key. The default implementation is to return
    the empty string, meaning that all URLs would be mapped to the same file system instance. However, derived classes
    can override _get_fs_url_key to customize rules for mapping URLs based on e.g. whether they are in the same bucket,
    whether they require the same credentials, etc.
    """
    def __init__(self) -> None: ...
    def reset_backend(self) -> None: ...
    def read_string_content_from_url(self, url: Url) -> str: ...
    def read_binary_content_from_url(self, url: Url) -> bytes: ...
    def delete_url(self, url: Url) -> None: ...
    def make_dirs(self, url: Url, exist_ok: bool = False) -> None: ...
    def get_file_size(self, url: Url) -> int: ...
    def exists(self, url: Url) -> bool: ...
    def is_dir(self, url: Url) -> bool: ...
    def is_writable(self, url: Url) -> bool:
        """Checks if a Url is writable.

        Actual implementation checks if the bucket is writable.
        """
    def list_dir(self, url: Url) -> Iterator[FSSpecUrlAdapterDirEntry]: ...
    def stat(self, url: Url) -> FSSpecUrlAdapterDirEntry:
        """Get status information for a file/directory.

        :param url: The URL of the file/directory to get status for
        :returns: A directory entry object containing file information
        :raises FileNotFoundError: If the URL does not exist
        """
    def touch(self, url: Url) -> None:
        """Update the last modified timestamp of a file to the current time.
        Creates the file if it doesn't exist.

        :param url: The URL of the file to touch
        """
