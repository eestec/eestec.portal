#!/usr/bin/env python
# -*- coding: utf-8 -*-

from eestec.portal.tests.base import IntegrationTestCase
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
        self.assertEquals(self.lc.title, u'Niš')

    def test_full_title(self):
        """Test the full_title() method of an LC."""
        self.assertEquals(self.lc.full_title(), u'Observer Niš')


class TestAddLC(IntegrationTestCase):
    """Test form for adding a new LC."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # prepare values for the new LC
        self.request.form['form.widgets.city'] = u'Niš'
        self.request.form['form.widgets.cp_username'] = u'jsmith'
        self.request.form['form.widgets.cp_fullname'] = u'Jöhn Smith'
        self.request.form['form.widgets.cp_email'] = u'john@eestec.net'

        # add the new LC
        self.form = self.portal.restrictedTraverse('@@add-lc')
        self.form.create()

    def test_lc_created(self):
        """Test that LC object was correctly created."""
        self.assertEquals(self.portal.lc['nis'].title, u'Niš')


def test_suite():
    """This sets up a test suite that actually runs the tests in the class
    above."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
