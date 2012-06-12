# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from eestec.portal.tests.base import IntegrationTestCase
from Products.CMFCore.utils import getToolByName

import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of eestec.portal into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = getToolByName(self.portal, 'portal_quickinstaller')

    def test_product_installed(self):
        """Test if eestec.portal is installed with portal_quickinstaller."""
        self.failUnless(self.installer.isProductInstalled('eestec.portal'))

    def test_uninstall(self):
        """Test if eestec.portal is cleanly uninstalled."""
        self.installer.uninstallProducts(['eestec.portal'])
        self.failIf(self.installer.isProductInstalled('eestec.portal'))

    # properties.xml
    def test_portal_title(self):
        """Test if portal title was correctly updated."""
        title = self.portal.getProperty('title')
        self.assertEquals("EESTEC International", title)

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IEestecPortalLayer is registered."""
        from eestec.portal.interfaces import IEestecPortalLayer
        from plone.browserlayer import utils
        self.failUnless(IEestecPortalLayer in utils.registered_layers())


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
