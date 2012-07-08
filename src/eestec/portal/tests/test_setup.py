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
        self.assertTrue(self.installer.isProductInstalled('eestec.portal'))

    def test_uninstall(self):
        """Test if eestec.portal is cleanly uninstalled."""
        self.installer.uninstallProducts(['eestec.portal'])
        self.assertFalse(self.installer.isProductInstalled('eestec.portal'))

    def test_dependencies_installed(self):
        """Test if eestec.portal's dependencies are installed."""
        self.assertFalse(self.installer.isProductInstalled('Dexterity Content Types'))
        self.assertFalse(self.installer.isProductInstalled('Diazo theme support'))
        self.assertFalse(self.installer.isProductInstalled('HTTP caching support'))
        self.assertFalse(self.installer.isProductInstalled('Niteoweb.LoginAs'))
        self.assertFalse(self.installer.isProductInstalled('Plone Toolbar'))

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
        self.assertTrue(IEestecPortalLayer in utils.registered_layers())

    # cssregistry.xml
    def test_css_registry_configured(self):
        css_resources = set(
            getToolByName(self.portal, 'portal_css').getResourceIds())

        self.failUnless(
            '++theme++eestec.portal/css/style.css' in css_resources)

    # jsregistry.xml
    def test_js_registry_configured(self):
        js_resources = set(
            getToolByName(self.portal, 'portal_javascripts').getResourceIds())

        self.failUnless(
            '++theme++eestec.portal/javascript/libs/modernizr.custom.js'
            in js_resources)
        self.failUnless(
            '++theme++eestec.portal/javascript/libs/respond.min.js'
            in js_resources)

    # index.html
    def test_doctype_configured(self):
        from plone.app.theming.interfaces import IThemeSettings
        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility

        settings = getUtility(IRegistry).forInterface(IThemeSettings)
        self.assertEqual(settings.doctype, '<!doctype html>')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
