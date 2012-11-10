# -*- coding: utf-8 -*-
"""Installer for this package."""

from setuptools import find_packages
from setuptools import setup

import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = \
    read('README.rst') + \
    read('docs', 'HISTORY.rst') + \
    read('docs', 'LICENSE.rst')

setup(
    name='eestec.portal',
    version='0.1',
    description="Enter description of what this project is all about.",
    long_description=long_description,
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='Plone Python',
    author='EESTEC International',
    author_email='it@eestec.com',
    url='http://eestec.net',
    license='BSD',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['eestec'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'collective.wtf',
        'collective.transmogrifier',
        'plone.app.transmogrifier',
        'quintagroup.transmogrifier',
        'niteoweb.loginas',
        'plone.api',
        'plone.behavior',
        'plone.app.caching',
        'plone.app.theming',
        # TODO: 'plone.app.event-ploneintegration',
        'plone.app.dexterity [grok]',
        'plone.app.versioningbehavior',
        'plone.app.toolbar',
        'plone.app.z3cform',
        'setuptools',
        'z3c.jbot',
        'z3c.schema',
        'five.pt',
        'Plone',
        'Pillow',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
            'plone.reload',
            'plone.app.debugtoolbar',
            'Products.Clouseau',
            'Products.DocFinderTab',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
            'zptlint',
            'pep8',
            'setuptools-flakes',
            'zest.releaser',
            'jarn.mkrelease',
            'Fabric',
        ],
        'production': [
            'Fabric',
        ]
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
