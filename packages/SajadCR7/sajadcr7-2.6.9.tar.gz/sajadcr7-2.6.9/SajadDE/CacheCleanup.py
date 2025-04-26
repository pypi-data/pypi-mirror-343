


""" Cleanup of caches for SajadQ.

This is triggered by "--clean-cache=" usage, and can cleanup all kinds of
caches and is supposed to run before or instead of SajadQ compilation.
"""

import os

from SajadDE.BytecodeCaching import getBytecodeCacheDir
from SajadDE.Tracing import cache_logger
from SajadDE.utils.AppDirs import getCacheDir
from SajadDE.utils.FileOperations import removeDirectory


def _cleanCacheDirectory(cache_name, cache_dir):
    from SajadDE.Options import shallCleanCache

    if shallCleanCache(cache_name) and os.path.exists(cache_dir):
        cache_logger.info(
            "Cleaning cache '%s' directory '%s'." % (cache_name, cache_dir)
        )
        removeDirectory(
            cache_dir,
            logger=cache_logger,
            ignore_errors=False,
            extra_recommendation=None,
        )
        cache_logger.info("Done.")


def cleanCaches():
    _cleanCacheDirectory("ccache", getCacheDir("ccache"))
    _cleanCacheDirectory("clcache", getCacheDir("clcache"))
    _cleanCacheDirectory("bytecode", getBytecodeCacheDir())
    _cleanCacheDirectory("dll-dependencies", getCacheDir("library_dependencies"))



