#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import ast
import setuptools

_version_re = re.compile(r'VERSION\s+=\s+(.*)')

with open('sierrapy/sierraclient.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def req(filename):
    with open(os.path.join(os.getcwd(), filename)) as fp:
        requires = set([strip_comments(l) for l in fp.readlines()])
        requires -= set([''])
    return list(requires)


setup_params = dict(
    name="sierrapy",
    version=version,
    url="https://github.com/hivdb/sierra-client/tree/master/python",
    author='Philip Tzou',
    author_email="philiptz@stanford.edu",
    description='A Client of HIVdb Sierra GraphQL Webservice.',
    packages=['sierrapy', 'sierrapy/fragments'],
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Bio-Informatics'],
    # test_suite="nose.collector",
    zip_safe=True)

if __name__ == '__main__':
    setuptools.setup(**setup_params)
