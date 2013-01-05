#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eestec.portal.tests.base import IntegrationTestCase
from eestec.portal import CP_LIST_ADDRESS
from eestec.portal import BOARD_LIST_ADDRESS
from email import message_from_string
from plone import api


class TestIntegration(IntegrationTestCase):
    """Integration tests for News Items."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.workflow = api.portal.get_tool('portal_workflow')

        # in tests we have to manually map content types to workflows
        self.workflow.setChainForPortalTypes(
            ['eestec.portal.event'],
            'event_workflow'
        )

        # add test item
        self.lc = api.content.create(
            type='eestec.portal.lc',
            title=u'lc',
            container=self.portal,
        )

        self.event = api.content.create(
            type='eestec.portal.event',
            title=u'Tést event',
            container=self.lc
        )

        self.event = self.portal.lc['test-event']

    def test_atevent_disabled(self):
        with self.assertRaises(ValueError):
            self.event = api.content.create(
                type='Event',
                title=u'Invalid event',
                container=self.lc
            )

    def test_notification_cp_email(self):
        """Test if notification email is sent to CP-list."""
        # publish the item
        api.content.transition(obj=self.event, transition='publish')
        mailhost = api.portal.get_tool('MailHost')
        self.assertEquals(len(mailhost.messages), 2)
        msg = message_from_string(mailhost.messages[1])

        self.assertEquals(msg['From'], 'EESTEC International <noreply@eestec.net>')
        self.assertEquals(msg['To'], CP_LIST_ADDRESS)
        self.assertEquals(msg['Subject'], '=?utf-8?q?=5BCP=5D_=5BEVENTS=5D_T=C3=A9st_event?=')
        self.assertIn('a new Event has been published', msg.get_payload())
        self.assertIn('http://nohost/plone/lc/test-event', msg.get_payload())

    def test_notification_cancellation_email(self):
        """Test if notification email is sent to Board-list upon cancellation."""
        api.content.transition(obj=self.event, transition='cancel')
        mailhost = api.portal.get_tool('MailHost')
        self.assertEquals(len(mailhost.messages), 2)
        msg = message_from_string(mailhost.messages[1])

        self.assertEquals(msg['From'], 'EESTEC International <noreply@eestec.net>')
        self.assertEquals(msg['To'], BOARD_LIST_ADDRESS)
        self.assertEquals(msg['Subject'], '=?utf-8?q?=5BEVENTS=5D=5BCancelled=5D_T=C3=A9st_event?=')
        self.assertIn('an Event has been cancelled', msg.get_payload())
        self.assertIn('http://nohost/plone/lc/test-event', msg.get_payload())

    def test_notification_creation_email(self):
        """Test if notification email is sent to Board-list upon creation."""
        mailhost = api.portal.get_tool('MailHost')
        self.assertEquals(len(mailhost.messages), 1)
        msg = message_from_string(mailhost.messages[0])

        self.assertEquals(msg['From'], 'EESTEC International <noreply@eestec.net>')
        self.assertEquals(msg['To'], BOARD_LIST_ADDRESS)
        self.assertEquals(msg['Subject'], '=?utf-8?q?=5BEVENTS=5D=5BCreated=5D_T=C3=A9st_event?=')
        self.assertIn('a new Event has been created', msg.get_payload())
        self.assertIn('T=C3=A9st event', msg.get_payload())
