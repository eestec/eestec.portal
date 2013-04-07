# -*- coding: utf-8 -*-
"""Base module for unit-testing."""

import unittest2 as unittest

from plone import api
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import z2
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost


class EestecPortalLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        import eestec.portal
        self.loadZCML(package=eestec.portal)
        self.loadZCML(package=eestec.portal, name='overrides.zcml')

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        applyProfile(portal, 'eestec.portal:default')

        # Mock MailHost
        mockmailhost = MockMailHost('MailHost')
        mockmailhost.smtp_host = 'nohost'
        portal.MailHost = mockmailhost
        sm = api.portal.get().getSiteManager()
        sm.registerUtility(component=mockmailhost, provided=IMailHost)

        # Give TEST_USER Manager role and login
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'eestec.portal')


FIXTURE = EestecPortalLayer()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="EestecPortalLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="EestecPortalLayer:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING

    def login(self, username=None, password=None):

        if not username:
            username = TEST_USER_NAME

        if not password:
            password = TEST_USER_PASSWORD

        self.browser.open(self.layer['portal'].absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = username
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()
