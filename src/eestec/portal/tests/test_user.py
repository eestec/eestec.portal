#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date
from eestec.portal.tests.base import IntegrationTestCase
from plone import api


class TestUserFields(IntegrationTestCase):
    """Test eestec User
    """

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def test_adapter_registration(self):
        """Test that self.portal is adapted by IEestecPortalUserDataSchema."""
        from eestec.portal.content.user import IEestecPortalUserDataSchema
        adapter = IEestecPortalUserDataSchema(self.portal)
        self.assertNotEquals(adapter, None)

    def test_fields_set_upon_user_creation(self):
        """Test that fields are correctly set when a user is created."""
        self.user = api.user.create(
            email='lois@plone.org',
            username='lois',
            properties=dict(
                lc=u'Quahog',
                mobile=u'666',
                study_field=u'housewife',
                birthdate=date(1960, 7, 22),
                sex=u'Female',
                nationality=u'USA',
                address=u'Rhode Island',
                passport_id=u'666',
                passport_date_of_issue=date.today(),
                passport_valid_until=date.today(),
                tshirt_size=u'Large',
                needs=u'No needs'
            )
        )

        self.assertEquals(self.user.getProperty('lc'), u'Quahog')
        self.assertEquals(self.user.getProperty('mobile'), u'666')
        self.assertEquals(self.user.getProperty('study_field'), u'housewife')
        self.assertEquals(self.user.getProperty('birthdate'), date(1960, 7, 22))
        self.assertEquals(self.user.getProperty('sex'), u'Female')
        self.assertEquals(self.user.getProperty('nationality'), u'USA')
        self.assertEquals(self.user.getProperty('address'), u'Rhode Island')
        self.assertEquals(self.user.getProperty('passport_id'), u'666')
        self.assertEquals(self.user.getProperty('tshirt_size'), u'Large')
        self.assertEquals(self.user.getProperty('needs'), u'No needs')
        self.assertEquals(
            self.user.getProperty('passport_date_of_issue'),
            date.today()
        )
        self.assertEquals(
            self.user.getProperty('passport_valid_until'),
            date.today()
        )
