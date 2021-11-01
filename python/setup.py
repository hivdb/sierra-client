#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import sys
import ast
import setuptools  # type: ignore

from typing import Optional, List


_version_re: re.Pattern = re.compile(r'VERSION\s+=\s+(.*)')

with open('sierrapy/sierraclient.py', 'rb') as f:
    ver_match: Optional[re.Match] = _version_re.search(
        f.read().decode('utf-8')
    )
    if not ver_match:
        print(
            'Unable to find version from sierrapy/sierraclient.py',
            file=sys.stderr
        )
        exit(1)
    version: str = str(ast.literal_eval(ver_match.group(1)))


def strip_comments(line: str) -> str:
    if line.startswith('-i '):
        return ''
    return line.split('#', 1)[0].strip()


def req(filename: str) -> List[str]:
    ln: str
    requires: set
    with open(os.path.join(os.getcwd(), filename)) as fp:
        requires = set([strip_comments(ln) for ln in fp.readlines()])
        requires -= set([''])
    return list(requires)


setup_params = dict(
    name="sierrapy",
    version=version,
    url="https://github.com/hivdb/sierra-client/tree/master/python",
    author='Philip Tzou',
    author_email="philiptz@stanford.edu",
    description='A Client of HIVdb Sierra GraphQL Webservice.',
    packages=['sierrapy', 'sierrapy/fragments',
              'sierrapy/recipes', 'sierrapy/commands'],
    install_requires=req('requirements.txt'),
    # tests_require=reqs('test-requirements.txt'),
    include_package_data=True,
    entry_points={'console_scripts': [
        'sierrapy = sierrapy.cmds:main',
    ]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Bio-Informatics'],
    # test_suite="nose.collector",
    zip_safe=True)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
