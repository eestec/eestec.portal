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
        # TODO: 'plone.app.event-ploneintegration',
        'collective.wtf',
        'five.pt',
        'niteoweb.loginas',
        'Pillow',
        'Plone',
        'plone.api',
        'plone.app.caching',
        'plone.app.dexterity [grok]',
        'plone.app.theming',
        'plone.app.toolbar',
        'plone.app.versioningbehavior',
        'plone.app.z3cform',
        'plone.behavior',
        'setuptools',
        'z3c.jbot',
        'z3c.schema',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.testing',
            'unittest2',
        ],
        'develop': [
            'Fabric',
            'flake8',
            'jarn.mkrelease',
            'plone.app.debugtoolbar',
            'plone.reload',
            'Products.Clouseau',
            'Products.DocFinderTab',
            'Products.PDBDebugMode',
            'Products.PrintingMailHost',
            'quintagroup.transmogrifier',
            'Sphinx',
            'transmogrify.dexterity',
            'zest.releaser',
            'zptlint',
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
