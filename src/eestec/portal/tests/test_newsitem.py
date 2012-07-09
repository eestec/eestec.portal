# -*- coding: utf-8 -*-
"""Testing News Items."""

from eestec.portal.tests.base import FunctionalTestCase
from eestec.portal.tests.base import IntegrationTestCase
from email import message_from_string
from plone import api
from plone.api import content
from plone.testing.z2 import Browser


class TestIntegration(IntegrationTestCase):
    """Integration tests for News Items."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.workflow = api.get_tool('portal_workflow')

        # content types don't have assigned workflows in tests, we have to
        # set them explicitly
        self.workflow.setChainForPortalTypes(
            ['News Item'],
            'simple_publication_workflow'
        )

        # add test item TODO: replace with api call
        content.create(
            type='News Item',
            title='Tést item',
            container=self.portal
        )
        self.newsitem = self.portal['test-item']

        # publish the item
        content.transition(obj=self.newsitem, transition='publish')

    def test_notification_email(self):
        """Test if notification email is sent to CP-list."""
        mailhost = api.get_tool('MailHost')
        self.assertEquals(len(mailhost.messages), 1)
        msg = message_from_string(mailhost.messages[0])

        self.assertEquals(msg['From'], 'EESTEC International <noreply@eestec.net>')
        self.assertEquals(msg['To'], 'cp@eestec.net')
        self.assertEquals(msg['Subject'], '=?utf-8?q?=5BCP=5D_=5BNEWS=5D_T=C3=A9st_item?=')
        self.assertIn('a new News Item has been published', msg.get_payload())
        self.assertIn('http://nohost/plone/test-item', msg.get_payload())


class TestFunctional(FunctionalTestCase):
    """Full-blown browser tests for News Items."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.workflow = api.get_tool('portal_workflow')
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.login()  # login with self.browser so we can add content

    def test_image_is_required(self):
        """Try to add a News Item without an image."""

        # go to add form
        self.browser.open('http://nohost/plone/createObject?type_name=News+Item')

        # fill in the title field (leave the rest empty)
        self.browser.getControl('Title').value = u"Test item"

        # click Save
        self.browser.getControl('Save').click()

        # check if `required` error is there
        self.assertRegexpMatches(
            self.browser.url,
            'http://nohost/plone/portal_factory/News%20Item/news_item.[^/]+/atct_edit'
        )
        self.assertIn(
            'Image is required, please correct.',
            self.browser.contents
        )