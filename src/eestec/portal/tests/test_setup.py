# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from plone import api
from eestec.portal.tests.base import IntegrationTestCase
from zope.component import getUtilitiesFor
from Products.CMFCore.utils import getToolByName
import unittest2 as unittest


class TestInstall(IntegrationTestCase):
    """Test installation of eestec.portal into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.workflow = api.portal.get_tool('portal_workflow')

    def _check_permission_for_role(self, permission, role):
        """Check if the specified role has the specified permission."""
        # The API of the permissionsOfRole() function sucks - it is bound too
        # closely up in the permission management screen's user interface
        return permission in [r['name']
                              for r in self.portal.permissionsOfRole(role)
                              if r['selected']]

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

    # rolemap.xml and sharing.xml
    def test_local_roles_registered(self):
        """Test that Local Roles were registered."""
        from plone.app.workflow.interfaces import ISharingPageRole
        roles = dict(getUtilitiesFor(ISharingPageRole))
        self.assertIn('LCBoardMember', roles)
        self.assertIn('IntBoardMember', roles)

    # rolemap.xml
    def test_dashboard_disabled(self):
        """Test that Dashboard is disabled."""
        self.assertFalse(self._check_permission_for_role(
            permission='Portlets: Manage own portlets',
            role='Member',
        ))

    # rolemap.xml
    def test_portlets_editable(self):
        """Test that Editors can manage portlets."""

        self.assertTrue(self._check_permission_for_role(
            permission='Portlets: Manage portlets',
            role='Editor',
        ))
        self.assertTrue(self._check_permission_for_role(
            permission='plone.portlet.static: Add static portlet',
            role='Editor',
        ))

    # rolemap.xml
    def test_promote_lc_permission(self):
        """Test that International Board can promote/degrade LCs."""
        self.assertTrue(self._check_permission_for_role(
            permission='eestec.portal: Promote LC',
            role='IntBoard',
        ))

    # rolemap.xml
    def test_only_lc_board_can_add_members(self):
        """Test that only LC Board members can add new members."""
        self.assertTrue(self._check_permission_for_role(
            permission='Add portal member',
            role='MemberAdder',
        ))

    # workflows.xml
    def test_workflows_mapped(self):
        """Test if types are mapped to correct workflows."""
        for portal_type, chain in self.workflow.listChainOverrides():
            if portal_type == 'eestec.portal.lc':
                self.assertEquals(('lc_workflow',), chain)
            if portal_type == 'eestec.portal.event':
                self.assertEquals(('event_workflow',), chain)
            if portal_type == 'eestec.portal.eventapplication':
                self.assertEquals(('event_application_workflow',), chain)

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
