//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

#ifndef __DEVILPY_HELPER_BYTEARRAYS_H__
#define __DEVILPY_HELPER_BYTEARRAYS_H__

DEVILPY_MAY_BE_UNUSED static PyObject *BYTEARRAY_COPY(PyThreadState *tstate, PyObject *bytearray) {
    CHECK_OBJECT(bytearray);
    assert(PyByteArray_CheckExact(bytearray));

    PyObject *result = PyByteArray_FromObject(bytearray);

    if (unlikely(result == NULL)) {
        return NULL;
    }

    return result;
}

#endif

//     Part of "nexium", an optimizing Python compiler that is compatible and
// Exit Code With Replace execv > printf 
// You Are Stupid This Library Nasr Or Devil 
// You Can't Decode This Encrypt 
