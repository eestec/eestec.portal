#!/usr/bin/env python
# -*- coding: utf-8 -*-


from eestec.portal.tests.base import IntegrationTestCase
from plone import api
from plone.api import content


class TestContent(IntegrationTestCase):
    """Test eestec content types."""

    def setUp(self):
        """docstring for setUp"""
        self.portal = self.layer['portal']
        self.workflow = api.get_tool('portal_workflow')

        # in tests we have to manually map content types to workflows
        self.workflow.setDefaultChain('lc_workflow')

        # create an LC
        content.create(
            type='eestec.portal.lc',
            title=u'Niš',
            container=self.portal
        )
        self.lc = self.portal['nis']

    def test_city(self):
        """Test that LC's city is set correctly."""
        self.assertEquals(self.lc.title, u'Niš')

    def test_full_lc_title(self):
        """Test the full_lc_title() method of an LC."""
        self.assertEquals(self.lc.full_lc_title(), u'Observer Niš')
