#include <Python.h>

static PyObject* hello(PyObject* self) {
    return PyUnicode_FromString("Hello from C!");
}

static PyMethodDef methods[] = {
    {"hello", (PyCFunction)hello, METH_NOARGS, "测试C扩展"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "accelerate",
    NULL,
    -1,
    methods
};

PyMODINIT_FUNC PyInit_accelerate(void) {
    return PyModule_Create(&module);
}