# -*- coding: utf-8 -*-
"""Testing LC content type."""

from eestec.portal.content.lc import AddForm
from eestec.portal.tests.base import IntegrationTestCase
from email import message_from_string
from plone import api

import unittest2 as unittest


class TestLC(IntegrationTestCase):
    """Test eestec LC type."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.workflow = api.portal.get_tool('portal_workflow')

        # in tests we have to manually map content types to workflows
        self.workflow.setDefaultChain('lc_workflow')

        # create an LC
        api.content.create(
            type='eestec.portal.lc',
            title=u'Niš',
            container=self.portal
        )
        self.lc = self.portal['nis']

    def test_city(self):
        """Test that LC's city is set correctly."""
        self.assertEqual(self.lc.title, u'Niš')

    def test_full_title(self):
        """Test the full_title() method of an LC."""
        self.assertEqual(self.lc.full_title(), u'Observer Niš')


class TestAddLC(IntegrationTestCase):
    """Test form for adding a new LC."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # prepare request values for the new LC
        self.request.form['form.widgets.city'] = u'Niš'
        self.request.form['form.widgets.cp_username'] = 'jsmith'
        self.request.form['form.widgets.cp_fullname'] = u'Jöhn Smith'
        self.request.form['form.widgets.cp_email'] = 'john@eestec.net'

        # Create the 'LC' folder
        api.content.create(
            type='Folder', id='lc', container=self. portal)

        # call the AddForm's create() method to create us a new LC
        AddForm(self.portal, self.request).create()

    def test_lc_created(self):
        """Test that LC object was correctly created."""
        self.assertEqual(self.portal.lc['nis'].title, u'Niš')

    def test_cp_user_created(self):
        """Test that a member object is created for CP."""
        self.assertTrue(api.user.get(username='jsmith'))

    def test_lc_members_group_created(self):
        """Test that LC members group is created when LC is added and that
        CP is a member of this group."""
        # LC members group exists
        self.assertTrue(api.group.get(groupname='nis-members'))

        # CP is member of LC Members group
        self.assertIn(
            'nis-members',
            [group.id for group in api.group.get_groups(username='jsmith')]
        )

        # LC Members can:
        self.assertItemsEqual(
            [
                'Authenticated',  # virtual group
                'Contributor',    # add content to their LC
            ],
            api.group.get_roles(
                groupname='nis-members',
                obj=self.portal.lc['nis'],
            )
        )

    def test_lc_boardies_group_created(self):
        """Test that LC members group is created when LC is added and that
        CP is a member of this group."""
        # LC Board group exists
        self.assertTrue(api.group.get('nis-board'))

        # CP is member of the LC Board group
        self.assertIn(
            'nis-board',
            [group.id for group in api.group.get_groups(username='jsmith')]
        )

        # LC Boardies can:
        self.assertItemsEqual(
            [
                'Authenticated',  # virtual group
                'Contributor',    # add content to their LC
                'MemberAdder',    # add new members
                'Reader',         # view private content in their LC
                'Reviewer',       # publish content in their LC
            ],
            api.group.get_roles(
                groupname='nis-board',
                obj=self.portal.lc['nis'],
            )
        )

        # The MemberAdder role needs to be global, not only local on the LC
        self.assertIn(
            'MemberAdder',
            api.group.get_roles(groupname='nis-board')
        )

    def test_email_notification_sent(self):
        """Test that the confirmation email was correctly sent."""
        mailhost = api.portal.get_tool('MailHost')
        self.assertEqual(len(mailhost.messages), 1)
        msg = message_from_string(mailhost.messages[0])

        self.assertEqual(msg['From'], 'admin@mysite.com')
        self.assertEqual(msg['To'], 'john@eestec.net')
        self.assertIn('your LC was added to our database', msg.get_payload())
        self.assertIn('mail_password_form?userid=3Djsmith', msg.get_payload())
        self.assertEqual(
            msg['Subject'],
            '=?utf-8?q?=5BEESTEC_Website=5D_registration_completed?='
        )


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
