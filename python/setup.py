#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import setuptools  # type: ignore

from typing import List

VERSION = '0.4.3'


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
    version=VERSION,
    url="https://github.com/hivdb/sierra-client/tree/master/python",
    author='Philip Tzou',
    author_email="philiptz@stanford.edu",
    description='A Client of HIVdb Sierra GraphQL Webservice.',
    packages=['sierrapy',
              'sierrapy/fragments',
              'sierrapy/recipes',
              'sierrapy/commands',
              'sierrapy/viruses'],
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
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering :: Bio-Informatics'],
    # test_suite="nose.collector",
    zip_safe=True)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
