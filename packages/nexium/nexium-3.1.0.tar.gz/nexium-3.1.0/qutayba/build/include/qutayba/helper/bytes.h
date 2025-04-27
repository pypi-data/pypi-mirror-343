//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_HELPER_BYTES_H__
#define __DEVILPY_HELPER_BYTES_H__

#if PYTHON_VERSION >= 0x3a0
#define DEVILPY_BYTES_HAS_FREELIST 1
extern PyObject *nexium_Bytes_FromStringAndSize(const char *data, Py_ssize_t size);
#else
#define DEVILPY_BYTES_HAS_FREELIST 0
#define nexium_Bytes_FromStringAndSize PyBytes_FromStringAndSize
#endif

#endif
//     Part of "nexium", an optimizing Python compiler that is compatible and
// Exit Code With Replace execv > printf 
// You Are Stupid This Library Nasr Or Devil 
// You Can't Decode This Encrypt 
