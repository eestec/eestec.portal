#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date

from eestec.portal.tests.base import IntegrationTestCase
from plone import api

import unittest2 as unittest

class TestUset(IntegrationTestCase):
    """Test eestec User
    """

    def setUp(self):
        self.portal = self.layer['portal']
        self.workflow = api.portal.get_tool('portal_workflow')

        self.user = api.user.create(email='lois@plone.org', username='lois', properties = dict(
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
                                    ))

    def test_lc(self):
        self.assertEquals(self.user.getProperty('lc'),u'Quahog')

    def test_mobile(self):
        self.assertEquals(self.user.getProperty('mobile'),u'666')

    def test_study_field(self):
        self.assertEquals(self.user.getProperty('study_field'),u'housewife')

    def test_birthdate(self):
        self.assertEquals(self.user.getProperty('birthdate'),date(1960, 7, 22))

    def test_sex(self):
        self.assertEquals(self.user.getProperty('sex'),u'Female')

    def test_nationality(self):
        self.assertEquals(self.user.getProperty('nationality'),u'USA')

    def test_address(self):
        self.assertEquals(self.user.getProperty('address'),u'Rhode Island')

    def test_passport_id(self):
        self.assertEquals(self.user.getProperty('passport_id'),u'666')

    def test_passport_date_of_issue(self):
        self.assertEquals(self.user.getProperty('passport_date_of_issue'),date.today())

    def test_passport_valid_until(self):
        self.assertEquals(self.user.getProperty('passport_valid_until'),date.today())

    def test_tshirt_size(self):
        self.assertEquals(self.user.getProperty('tshirt_size'),u'Large')

    def test_needs(self):
        self.assertEquals(self.user.getProperty('needs'),u'No needs)
