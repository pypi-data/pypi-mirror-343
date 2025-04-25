# Copyright 2025 Kasma
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import py_compile
import fnmatch
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as build_py_orig
import sys

excluded = [
    "_client.py",
    "utils/json.py",
]


def compile_excluded_files():
    os.chdir("src/flavius")
    pyc_files = []
    for src_file in excluded:
        pyc_file = f"{src_file}c"
        py_compile.compile(src_file, cfile=pyc_file)
        pyc_files.append(pyc_file)
    os.chdir("../..")
    return pyc_files


class BuildPy(build_py_orig):
    def find_package_modules(self, package, package_dir):
        modules = super().find_package_modules(package, package_dir)
        return [
            (pkg, mod, file)
            for (pkg, mod, file) in modules
            if not any(fnmatch.fnmatchcase(file, pat=pattern) for pattern in excluded)
        ]


name_base = "flavius"
with_python_version = os.getenv("WITH_PYTHON_VERSION")
if with_python_version == "1":
    python_version = f"py{sys.version_info.major}{sys.version_info.minor}"
    name = f"{name_base}-{python_version}"
else:
    name = name_base

setup(
    name=name,
    version="0.2.0",
    author="Kasma, Inc.",
    description="A Python client for Flavius",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords=["flavius", "graph", "database"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "flavius": compile_excluded_files(),
    },
    cmdclass={"build_py": BuildPy},
    install_requires=[
        "requests>=2.32.3",
        "python-dateutil>=2.9.0.post0",
    ],
)
