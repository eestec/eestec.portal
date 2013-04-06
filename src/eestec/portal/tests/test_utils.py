# -*- coding: utf-8 -*-
"""Tests for utility methods."""

from eestec.portal.tests.base import IntegrationTestCase

import unittest2 as unittest


class TestUtils(IntegrationTestCase):
    """Test eestec.portal utils.."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']

    def test_get_portal_from(self):
        """Test if portal_from email address is correctly formatted."""
        from eestec.portal.utils import get_portal_from
        self.assertEqual(
            get_portal_from(),
            'EESTEC International <noreply@eestec.net>'
        )


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
