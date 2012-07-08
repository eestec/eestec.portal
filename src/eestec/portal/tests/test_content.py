#!/usr/bin/env python
# -*- coding: utf-8 -*-
from eestec.portal.tests.base import IntegrationTestCase

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles


class TestContent(IntegrationTestCase):
    """Test eestec content types."""

    def setUp(self):
        """docstring for setUp"""
        self.portal = self.layer['portal']

    def test_hierarchy(self):
        """Ensure that we can create the content types without an error"""
        setRoles(self.portal, TEST_USER_ID, ('Manager',))

        self.portal.invokeFactory(
            'eestec.portal.lc', 'lc1',
            title=u'LC Šiška',
            description=u'Imaginary LC'
        )

    def test_full_lc_title(self):
        """TODO"""
        pass
