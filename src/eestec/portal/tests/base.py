# -*- coding: utf-8 -*-
"""Base module for unit-testing."""

import unittest2 as unittest

from plone import api
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.testing import z2
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost

import eestec.portal


class EestecPortalLayer(PloneWithPackageLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        super(EestecPortalLayer, self).setUpZope(app, configurationContext)
        self.loadZCML(package=eestec.portal, name='overrides.zcml')

    def setUpPloneSite(self, portal):
        super(EestecPortalLayer, self).setUpPloneSite(portal)

        # Mock MailHost
        mockmailhost = MockMailHost('MailHost')
        mockmailhost.smtp_host = 'nohost'
        portal.MailHost = mockmailhost
        sm = api.portal.get().getSiteManager()
        sm.registerUtility(component=mockmailhost, provided=IMailHost)

        # Login
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)

        # Rebuild the catalog and commit changes
        portal.portal_catalog.clearFindAndRebuild()
        import transaction
        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        z2.uninstallProduct(app, 'eestec.portal')  # TODO: move to plone.app.testing


FIXTURE = EestecPortalLayer(zcml_filename='configure.zcml',
                            zcml_package=eestec.portal,
                            gs_profile_id='eestec.portal:default',
                            additional_z2_products=('eestec.portal',))
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,),
                                         name="EestecPortalLayer:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,),
                                       name="EestecPortalLayer:Functional")


class TestBase(unittest.TestCase):
    """Place to throw in utility methods used in our tests."""

    def _add_lc(self, city=u'Niš', cp_username='jsmith',
                cp_fullname=u'Jöhn Smith', cp_email='john@eestec.net'):
        """Helper method to add a new LC"""

        # prepare request values for the new LC
        request = self.layer['request']
        request.form['form.widgets.city'] = u'Niš'
        request.form['form.widgets.cp_username'] = u'jsmith'
        request.form['form.widgets.cp_fullname'] = u'Jöhn Smith'
        request.form['form.widgets.cp_email'] = u'john@eestec.net'

        # call the @@add-lc form to create us a new LC
        self.layer['portal'].restrictedTraverse('@@add-lc').create()


class IntegrationTestCase(TestBase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(TestBase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING

    def login(self):
        self.browser.open(self.layer['portal'].absolute_url() + '/login_form')
        self.browser.getControl(name='__ac_name').value = TEST_USER_NAME
        self.browser.getControl(name='__ac_password').value = TEST_USER_PASSWORD
        self.browser.getControl(name='submit').click()
