#!/usr/bin/env python
"""
sentry-groveio
==============

An extension for Sentry which integrates with Grove.io. It will forward
notifications to an IRC room.

:copyright: (c) 2012 by Matt Robenolt, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
from setuptools import setup, find_packages


tests_require = [
    'nose>=1.1.2',
]

install_requires = [
    'sentry>=5.0.0',
]

setup(
    name='sentry-groveio',
    version='0.2.0',
    author='Matt Robenolt',
    author_email='matt@ydekproductons.com',
    url='http://github.com/mattrobenolt/sentry-groveio',
    description='A Sentry extension which integrates with Grove.io.',
    long_description=__doc__,
    license='BSD',
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    test_suite='runtests.runtests',
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'groveio = sentry_groveio',
        ],
        'sentry.plugins': [
            'groveio = sentry_groveio.models:GroveIoPlugin',
        ]
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
