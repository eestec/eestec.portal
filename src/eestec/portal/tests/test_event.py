#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eestec.portal.tests.base import IntegrationTestCase

from plone.api import content
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


class TestEvent(IntegrationTestCase):

    def setUp(self):
        self.portal = self.layer['portal']

    def test_hierarchy(self):
        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        lc = content.create(
            type='eestec.portal.lc',
            title=u'lc',
            container=self.portal,
        )

        event = content.create(
            type='eestec.portal.event',
            id=u'event',
            container=lc,
        )
