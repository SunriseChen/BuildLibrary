#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
NTFS 符号连接的创建、读取等功能。
'''

# pylint: disable=C0325,W0401,C0412,W0622,W0612,C0103

import ctypes
import os
import struct
import sys

try:
    from win32file import *
except ImportError:
    from ctypes import windll, wintypes


    def GetFileAttributes(fileName):
        '''GetFileAttributes'''
        if not isinstance(fileName, unicode):
            fileName = unicode(fileName)
        return windll.kernel32.GetFileAttributesW(fileName)


    def CreateFile(fileName, desiredAccess, shareMode, securityAttributes,
                   creationDisposition, flagsAndAttributes, templateFile):
        '''CreateFile'''
        if not isinstance(fileName, unicode):
            fileName = unicode(fileName)
        return windll.kernel32.CreateFileW(fileName, desiredAccess, shareMode,
                                           securityAttributes, creationDisposition,
                                           flagsAndAttributes, templateFile)


    _DeviceIoControl = windll.kernel32.DeviceIoControl
    _DeviceIoControl.argtypes = (
        wintypes.HANDLE,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    )
    _DeviceIoControl.restype = wintypes.BOOL

    def DeviceIoControl(device, ioControlCode, inBuffer, outBuffer, overlapped=None):
        '''DeviceIoControl'''
        inBufferSize = len(inBuffer) if inBuffer else 0
        if isinstance(outBuffer, int):
            outBuffer = ctypes.create_string_buffer(outBuffer)
        outBufferSize = len(outBuffer)
        if not isinstance(outBuffer, ctypes.Array):
            return None
        bytesReturned = wintypes.DWORD()
        status = _DeviceIoControl(device, ioControlCode, inBuffer, inBufferSize,
                                  outBuffer, outBufferSize, bytesReturned, overlapped)
        if status == 0:
            raise ctypes.WinError()

        return outBuffer[:bytesReturned.value]


    CloseHandle = windll.kernel32.CloseHandle


    def CreateSymbolicLink(symlinkFileName, targetFileName, flags):
        '''CreateSymbolicLink'''
        if not isinstance(symlinkFileName, unicode):
            symlinkFileName = unicode(symlinkFileName)
        if not isinstance(targetFileName, unicode):
            targetFileName = unicode(targetFileName)
        return windll.kernel32.CreateSymbolicLinkW(symlinkFileName, targetFileName, flags)


INVALID_FILE_ATTRIBUTES = -1
FILE_ATTRIBUTE_REPARSE_POINT = 1024

GENERIC_READ = 0x80000000
OPEN_EXISTING = 3
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_REPARSE_BACKUP = FILE_FLAG_OPEN_REPARSE_POINT | FILE_FLAG_BACKUP_SEMANTICS

FSCTL_GET_REPARSE_POINT = 0x000900A8


def supports_symlinks():
    '''supports_symlinks'''
    return sys.getwindowsversion()[0] >= 6


def islink(path):
    """ Windows islink implementation. """
    attrs = GetFileAttributes(path)
    if attrs == INVALID_FILE_ATTRIBUTES:
        return False

    return attrs & FILE_ATTRIBUTE_REPARSE_POINT == FILE_ATTRIBUTE_REPARSE_POINT


# 参考：http://stackoverflow.com/questions/1447575/symlinks-on-windows
def readlink(path):
    """ Windows readlink implementation. """
    if not islink(path):
        return None

    handle = CreateFile(path, GENERIC_READ, 0, None, OPEN_EXISTING, FILE_FLAG_REPARSE_BACKUP, None)

    # 参考：http://msdn.microsoft.com/en-us/library/windows/desktop/aa364571(v=vs.85).aspx
    # MAXIMUM_REPARSE_DATA_BUFFER_SIZE = 16384 = (16*1024)
    buffer = DeviceIoControl(handle, FSCTL_GET_REPARSE_POINT, None, 16*1024)
    CloseHandle(handle)

    if not buffer or len(buffer) < 9:
        return None

    # 参考：http://msdn.microsoft.com/en-us/library/ff552012.aspx
    #typedef struct _REPARSE_DATA_BUFFER {
    #  ULONG  ReparseTag;
    #  USHORT ReparseDataLength;
    #  USHORT Reserved;
    #  union {
    #    struct {
    #      USHORT SubstituteNameOffset;
    #      USHORT SubstituteNameLength;
    #      USHORT PrintNameOffset;
    #      USHORT PrintNameLength;
    #      ULONG  Flags;
    #      WCHAR  PathBuffer[1];
    #    } SymbolicLinkReparseBuffer;
    #    struct {
    #      USHORT SubstituteNameOffset;
    #      USHORT SubstituteNameLength;
    #      USHORT PrintNameOffset;
    #      USHORT PrintNameLength;
    #      WCHAR  PathBuffer[1];
    #    } MountPointReparseBuffer;
    #    struct {
    #      UCHAR DataBuffer[1];
    #    } GenericReparseBuffer;
    #  };
    #} REPARSE_DATA_BUFFER, *PREPARSE_DATA_BUFFER;
    symbolicLinkReparseFormat = 'LHHHHHHL'
    symbolicLinkReparseSize = struct.calcsize(symbolicLinkReparseFormat)

    (reparseTag, reparseDataLength, reserved,
     substituteNameOffset, substituteNameLength,
     printNameOffset, printNameLength, flags) = struct.unpack(
         symbolicLinkReparseFormat, buffer[:symbolicLinkReparseSize])

    start = symbolicLinkReparseSize + substituteNameOffset
    target = buffer[start : start + substituteNameLength].decode('utf-16')

    ending = target.find(u'\0')
    if ending > 0:
        target = target[:ending]
    if target.startswith(u'\\\\?\\'):
        target = target[4:]

    return target if isinstance(path, unicode) else str(target)


if not callable(getattr(os, 'readlink', None)) and supports_symlinks():
    os.path.islink = islink
    os.readlink = readlink


def symlink(source, link_name):
    """ Windows symlink implementation. """
    flags = 1 if os.path.isdir(source) else 0
    if CreateSymbolicLink(link_name, source, flags) == 0:
        raise ctypes.WinError()


if not callable(getattr(os, 'symlink', None)) and supports_symlinks():
    os.symlink = symlink


def test():
    '''测试'''
    path = 'test_dir'
    if not os.path.exists(path):
        os.mkdir(path)
    assert not os.path.islink(path)
    link_name = 'link_dir'
    if not os.path.exists(link_name):
        os.symlink(path, link_name)
    assert os.path.islink(link_name)
    result = os.readlink(link_name)
    assert result == path, result
    os.rmdir(link_name)
    os.rmdir(path)
    print('Test passed !')


if __name__ == '__main__':
    test()
