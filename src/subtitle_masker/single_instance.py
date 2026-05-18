# -*- coding: utf-8 -*-
import ctypes
from ctypes import wintypes
import sys

from .version import APP_NAME


ERROR_ALREADY_EXISTS = 183
_SINGLE_INSTANCE_MUTEX = None


def is_another_instance_running():
    """Use a Windows named mutex to prevent multiple floating masks."""
    global _SINGLE_INSTANCE_MUTEX
    if sys.platform != "win32":
        return False

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.CreateMutexW.argtypes = (wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR)
    kernel32.CreateMutexW.restype = wintypes.HANDLE
    mutex_name = f"Local\\{APP_NAME}_SingleInstance"
    _SINGLE_INSTANCE_MUTEX = kernel32.CreateMutexW(None, False, mutex_name)
    if not _SINGLE_INSTANCE_MUTEX:
        return False

    return ctypes.get_last_error() == ERROR_ALREADY_EXISTS
