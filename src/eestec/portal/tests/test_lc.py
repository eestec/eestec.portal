#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plone import api

from eestec.portal.tests.base import IntegrationTestCase


class TestLC(IntegrationTestCase):
    """Test eestec LC type."""

    def setUp(self):
        """docstring for setUp"""
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
