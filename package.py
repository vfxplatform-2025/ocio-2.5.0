# -*- coding: utf-8 -*-
name = "ocio"
version = "2.5.0"
authors = ["Academy Software Foundation"]
description = "OpenColorIO color management framework"

requires = [
    "yaml_cpp-0.7.0",
    "pystring-1.1.3",
    "imath-3.1.9",
    "glew-2.1.0",
    "openexr-3.2.2",
    "lcms2-2.16",
    "minizip_ng-4.0.10"
]

build_requires = [
    "cmake-3.26.5",
    "gcc-11.5.0",
    "yaml_cpp-0.7.0",
    "pystring-1.1.3",
    "zlib-1.2.13",
    "glew-2.1.0",
    "freeglut-3.4.0",
    "python-3.13.2",
    "pybind11-2.11.1"
]

build_command = "python {root}/rezbuild.py {install}"

def commands():
    env.OCIO_ROOT = "{root}"
    env.CMAKE_PREFIX_PATH.append("{root}")
    env.PATH.append("{root}/bin")
    env.LD_LIBRARY_PATH.prepend("{root}/lib64")
#    env.LD_LIBRARY_PATH.prepend("/core/Linux/APPZ/packages/imath/3.1.9/lib64")  # ✨ 추가
#    env.LD_LIBRARY_PATH.prepend("/core/Linux/APPZ/packages/openexr/3.2.2/lib64")  # ✨ 추가 (권장)
    env.CPATH.prepend("{root}/include")
    env.PKG_CONFIG_PATH.prepend("{root}/lib64/pkgconfig")
    env.PYTHONPATH.prepend("{root}/lib64/python3.13/site-packages")


