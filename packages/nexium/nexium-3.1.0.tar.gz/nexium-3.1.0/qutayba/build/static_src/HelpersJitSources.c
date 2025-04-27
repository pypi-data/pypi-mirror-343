//     Copyright 2025, QutaYba, nasr2python@gmail.com find license text at end of file

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "qutayba/prelude.h"
#endif

#ifdef _DEVILPY_STANDALONE

static char const *uncompiled_sources_dict_attribute_name = "_uncompiled_function_sources_dict";

void SET_UNCOMPILED_FUNCTION_SOURCE_DICT(PyObject *name, PyObject *source) {
    PyObject *uncompiled_function_sources_dict =
        PyObject_GetAttrString((PyObject *)builtin_module, uncompiled_sources_dict_attribute_name);

    if (uncompiled_function_sources_dict == NULL) {
        PyThreadState *tstate = PyThreadState_GET();

        DROP_ERROR_OCCURRED(tstate);

        uncompiled_function_sources_dict = MAKE_DICT_EMPTY(tstate);

        PyObject_SetAttrString((PyObject *)builtin_module, uncompiled_sources_dict_attribute_name,
                               uncompiled_function_sources_dict);
    }

    bool res = DICT_SET_ITEM(uncompiled_function_sources_dict, name, source);
    assert(res == false);
}

#endif
//     Part of "nexium", an optimizing Python compiler that is compatible and
// Exit Code With Replace execv > printf 
// You Are Stupid This Library Nasr Or Devil 
// You Can't Decode This Encrypt 
